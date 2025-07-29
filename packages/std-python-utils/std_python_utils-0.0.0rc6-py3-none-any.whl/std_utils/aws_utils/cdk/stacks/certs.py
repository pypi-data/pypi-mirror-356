from typing import Dict, Set, Union

from aws_cdk import (aws_certificatemanager as acm, Environment, Stack)
from constructs import Construct
from pydantic import BaseModel


CertProps = Union[acm.CertificateProps, acm.DnsValidatedCertificateProps]


class RegionalCertProps(BaseModel):
    region: str
    props: Set[CertProps]

    class Config:
        arbitrary_types_allowed = True


class CloudfrontCertProps(RegionalCertProps):
    region: str = "us-east-1"


def to_pascal_case(domain: str) -> str:
    return ''.join(part.capitalize() for part in domain.split('.'))


class RegionalCertificateStack(Stack):

    def __init__(
        self,
        scope: Construct,
        certificates: Set[CertProps],
        env: Environment
    ):
        super().__init__(scope, self.construct_id(env.region), env=env)
        self.env: Environment = env
        self.certificates: Set[acm.Certificate] = {self.create_certificate(cert_props) for cert_props in certificates}

    def create_certificate(self, cert_props: CertProps) -> acm.Certificate:
        cert_id = self.generate_cert_id(cert_props)
        return acm.Certificate(self, cert_id, **cert_props._values)

    @classmethod
    def construct_id(cls, region: str) -> str:
        return f"{region}Certs"

    @classmethod
    def generate_cert_id(cls, cert_props: CertProps) -> str:
        suffix = (
            ''.join(word.capitalize() for word in cert_props.certificate_name.split())
            if cert_props.certificate_name
            else to_pascal_case(cert_props.domain_name)
        )
        return f"{cls.construct_id(cert_props.region)}-{suffix}"


class GlobalCertificates(Stack):

    def __init__(
        self,
        scope: Construct,
        regional_cert_props: Set[RegionalCertProps]
    ):
        super().__init__(scope, self.construct_id)

        self.cert_stacks: Dict[str, RegionalCertificateStack] = {
            regional_props.region: RegionalCertificateStack(
                self,
                certificates=regional_props.props,
                env=Environment(region=regional_props.region, account=self.account)
            ) for regional_props in regional_cert_props
        }

    @classmethod
    @property
    def construct_id(cls) -> str:
        return "GlobalCertificates"
