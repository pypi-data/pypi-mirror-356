#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import uuid
from abc import ABC
from itertools import product
from typing import Dict

from sunrise6g_opensdk import logger
from sunrise6g_opensdk.network.adapters.errors import NetworkPlatformError
from sunrise6g_opensdk.network.core import common, schemas

log = logger.get_logger(__name__)


def flatten_port_spec(ports_spec: schemas.PortsSpec | None) -> list[str]:
    has_ports = False
    has_ranges = False
    flat_ports = []
    if ports_spec and ports_spec.ports:
        has_ports = True
        flat_ports.extend([str(port) for port in ports_spec.ports])
    if ports_spec and ports_spec.ranges:
        has_ranges = True
        flat_ports.extend(
            [f"{range.from_.root}-{range.to.root}" for range in ports_spec.ranges]
        )
    if not has_ports and not has_ranges:
        flat_ports.append("0-65535")
    return flat_ports


def build_flows(
    flow_id: int,
    session_info: schemas.CreateSession,
) -> list[schemas.FlowInfo]:
    device_ports = flatten_port_spec(session_info.devicePorts)
    server_ports = flatten_port_spec(session_info.applicationServerPorts)
    ports_combis = list(product(device_ports, server_ports))

    device_ip = session_info.device.ipv4Address or session_info.device.ipv6Address
    if isinstance(device_ip, schemas.DeviceIpv6Address):
        device_ip = device_ip.root
    else:  # IPv4
        device_ip = (
            device_ip.root.publicAddress.root or device_ip.root.privateAddress.root
        )
    device_ip = str(device_ip)
    server_ip = (
        session_info.applicationServer.ipv4Address
        or session_info.applicationServer.ipv6Address
    )
    server_ip = server_ip.root
    flow_descrs = []
    for device_port, server_port in ports_combis:
        flow_descrs.append(
            f"permit in ip from {device_ip} {device_port} to {server_ip} {server_port}"
        )
        flow_descrs.append(
            f"permit out ip from {server_ip} {server_port} to {device_ip} {device_port}"
        )
    flows = [
        schemas.FlowInfo(flowId=flow_id, flowDescriptions=[", ".join(flow_descrs)])
    ]
    return flows


class BaseNetworkClient():
    """
    Class for Network Resource Management.

    This class provides shared logic and extension points for different
    Network 5G Cores (e.g., Open5GS, OAI, Open5GCore) interacting with
    NEF-like platforms using CAMARA APIs.
    """

    base_url: str
    scs_as_id: str

    def add_core_specific_qod_parameters(
        self,
        session_info: schemas.CreateSession,
        subscription: schemas.AsSessionWithQoSSubscription,
    ):
        """
        Placeholder for adding core-specific parameters to the subscription.
        This method should be overridden by subclasses to implement specific logic.
        """
        pass

    def add_core_specific_ti_parameters(
        self,
        traffic_influence_info: schemas.CreateTrafficInfluence,
        subscription: schemas.TrafficInfluSub,
    ):
        """
        Placeholder for adding core-specific parameters to the subscription.
        This method should be overridden by subclasses to implement specific logic.
        """
        pass

    def core_specific_qod_validation(self, session_info: schemas.CreateSession) -> None:
        """
        Validates core-specific parameters for the session creation.

        args:
            session_info: The session information to validate.

        raises:
            ValidationError: If the session information does not meet core-specific requirements.
        """
        # Placeholder for core-specific validation logic
        # This method should be overridden by subclasses if needed
        pass

    def core_specific_traffic_influence_validation(
        self, traffic_influence_info: schemas.CreateTrafficInfluence
    ) -> None:
        """
        Validates core-specific parameters for the session creation.

        args:
            session_info: The session information to validate.

        raises:
            ValidationError: If the session information does not meet core-specific requirements.
        """
        # Placeholder for core-specific validation logic
        # This method should be overridden by subclasses if needed
        pass

    def _build_qod_subscription(
        self, session_info: Dict
    ) -> schemas.AsSessionWithQoSSubscription:
        valid_session_info = schemas.CreateSession.model_validate(session_info)
        device_ipv4 = None
        if valid_session_info.device.ipv4Address:
            device_ipv4 = valid_session_info.device.ipv4Address.root.publicAddress.root

        self.core_specific_qod_validation(valid_session_info)
        subscription = schemas.AsSessionWithQoSSubscription(
            notificationDestination=str(valid_session_info.sink),
            qosReference=valid_session_info.qosProfile.root,
            ueIpv4Addr=device_ipv4,
            ueIpv6Addr=valid_session_info.device.ipv6Address,
            usageThreshold=schemas.UsageThreshold(duration=valid_session_info.duration),
        )
        self.add_core_specific_qod_parameters(valid_session_info, subscription)
        return subscription

    def _build_ti_subscription(self, traffic_influence_info: Dict):
        traffic_influence_data = schemas.CreateTrafficInfluence.model_validate(
            traffic_influence_info
        )
        self.core_specific_traffic_influence_validation(traffic_influence_data)

        device_ip = traffic_influence_data.retrieve_ue_ipv4()
        server_ip = (
            traffic_influence_data.appInstanceId
        )  # assume that the instance id corresponds to its IPv4 address
        sink_url = traffic_influence_data.notificationUri
        edge_zone = traffic_influence_data.edgeCloudZoneId

        # build flow descriptor in oai format using device ip and server ip
        flow_descriptor = f"permit out ip from {device_ip}/32 to {server_ip}/32"

        subscription = schemas.TrafficInfluSub(
            afAppId=traffic_influence_data.appId,
            ipv4Addr=str(device_ip),
            notificationDestination=sink_url,
        )
        subscription.add_flow_descriptor(flow_desriptor=flow_descriptor)
        subscription.add_traffic_route(dnai=edge_zone)

        self.add_core_specific_ti_parameters(traffic_influence_data, subscription)
        return subscription

    def create_qod_session(self, session_info: Dict) -> Dict:
        """
        Creates a QoS session based on CAMARA QoD API input.

        args:
            session_info: Dictionary containing session details conforming to
                          the CAMARA QoD session creation parameters.

        returns:
            dictionary containing the created session details, including its ID.
        """
        subscription = self._build_qod_subscription(session_info)
        response = common.as_session_with_qos_post(
            self.base_url, self.scs_as_id, subscription
        )
        subscription_info: schemas.AsSessionWithQoSSubscription = (
            schemas.AsSessionWithQoSSubscription(**response)
        )
        subscription_url = subscription_info.self_.root
        subscription_id = subscription_url.split("/")[-1] if subscription_url else None
        if not subscription_id:
            log.error("Failed to retrieve QoS session ID from response")
            raise NetworkPlatformError("QoS session ID not found in response")
        session_info = schemas.SessionInfo(
            sessionId=schemas.SessionId(uuid.UUID(subscription_id)),
            qosStatus=schemas.QosStatus.REQUESTED,
            **session_info,
        )
        return session_info.model_dump()

    def get_qod_session(self, session_id: str) -> Dict:
        """
        Retrieves details of a specific Quality on Demand (QoS) session.

        args:
            session_id: The unique identifier of the QoS session.

        returns:
            Dictionary containing the details of the requested QoS session.
        """
        session = common.as_session_with_qos_get(
            self.base_url, self.scs_as_id, session_id=session_id
        )
        log.info(f"QoD session retrived successfully [id={session_id}]")
        return session

    def delete_qod_session(self, session_id: str) -> None:
        """
        Deletes a specific Quality on Demand (QoS) session.

        args:
            session_id: The unique identifier of the QoS session to delete.

        returns:
            None
        """
        common.as_session_with_qos_delete(
            self.base_url, self.scs_as_id, session_id=session_id
        )
        log.info(f"QoD session deleted successfully [id={session_id}]")

    def create_traffic_influence_resource(self, traffic_influence_info: Dict) -> Dict:
        """
        Creates a Traffic Influence resource based on CAMARA TI API input.

        args:
            traffic_influence_info: Dictionary containing traffic influence details conforming to
                                    the CAMARA TI resource creation parameters.

        returns:
            dictionary containing the created traffic influence resource details, including its ID.
        """

        subscription = self._build_ti_subscription(traffic_influence_info)
        response = common.traffic_influence_post(
            self.base_url, self.scs_as_id, subscription
        )

        # retrieve the NEF resource id
        if "self" in response.keys():
            subscription_id = response["self"]
        else:
            subscription_id = None

        traffic_influence_info["trafficInfluenceID"] = subscription_id
        return traffic_influence_info

    def put_traffic_influence_resource(
        self, resource_id: str, traffic_influence_info: Dict
    ) -> Dict:
        """
        Retrieves details of a specific Traffic Influence resource.

        args:
            resource_id: The unique identifier of the Traffic Influence resource.

        returns:
            Dictionary containing the details of the requested Traffic Influence resource.
        """
        subscription = self._build_ti_subscription(traffic_influence_info)
        common.traffic_influence_put(
            self.base_url, self.scs_as_id, resource_id, subscription
        )

        traffic_influence_info["trafficInfluenceID"] = resource_id
        return traffic_influence_info

    def delete_traffic_influence_resource(self, resource_id: str) -> None:
        """
        Deletes a specific Traffic Influence resource.

        args:
            resource_id: The unique identifier of the Traffic Influence resource to delete.

        returns:
            None
        """
        common.traffic_influence_delete(self.base_url, self.scs_as_id, resource_id)
        return

    # Placeholder for other CAMARA APIs (e.g., Traffic Influence,
    # Location-retrieval, etc.)
