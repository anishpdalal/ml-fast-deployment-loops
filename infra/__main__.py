import pulumi
import pulumi_aws as aws

ml_vpc = aws.ec2.Vpc(
    "ml-vpc",
    cidr_block="10.0.0.0/16",
    enable_dns_hostnames=True,
    enable_dns_support=True
)
public_subnet_1 = aws.ec2.Subnet(
    "public-subnet-1",
    vpc_id=ml_vpc.id,
    cidr_block="10.0.1.0/24",
    availability_zone="us-east-1a"
)
public_subnet_2 = aws.ec2.Subnet(
    "public-subnet-2",
    vpc_id=ml_vpc.id,
    cidr_block="10.0.2.0/24",
    availability_zone="us-east-1b"
)
private_subnet_1 = aws.ec2.Subnet(
    "private-subnet-1",
    vpc_id=ml_vpc.id,
    cidr_block="10.0.3.0/24",
    availability_zone="us-east-1a"
)
private_subnet_2 = aws.ec2.Subnet(
    "private-subnet-2",
    vpc_id=ml_vpc.id,
    cidr_block="10.0.4.0/24",
    availability_zone="us-east-1b"
)
public_route_table = aws.ec2.RouteTable(
    "public-route-table",
    vpc_id=ml_vpc.id
)
private_route_table = aws.ec2.RouteTable(
    "private-route-table",
    vpc_id=ml_vpc.id
)
public_route_1_association = aws.ec2.RouteTableAssociation(
    "public-route-1-association",
    subnet_id=public_subnet_1.id,
    route_table_id=public_route_table.id
)
public_route_2_association = aws.ec2.RouteTableAssociation(
    "public-route-2-association",
    subnet_id=public_subnet_2.id,
    route_table_id=public_route_table.id
)
private_route_1_association = aws.ec2.RouteTableAssociation(
    "private-route-1-association",
    subnet_id=private_subnet_1.id,
    route_table_id=private_route_table.id
)
private_route_2_association = aws.ec2.RouteTableAssociation(
    "private-route-2-association",
    subnet_id=private_subnet_2.id,
    route_table_id=private_route_table.id
)
igw = aws.ec2.InternetGateway(
    "igw",
    vpc_id=ml_vpc.id
)
eip = aws.ec2.Eip(
    "elastic-ip-for-nat-gw",
    vpc=True,
    associate_with_private_ip="10.0.0.5",
    opts=pulumi.ResourceOptions(depends_on=[igw])
)
nat_gw = aws.ec2.NatGateway(
    "nat-gw",
    allocation_id=eip.id,
    subnet_id=public_subnet_1.id,
    opts=pulumi.ResourceOptions(depends_on=[eip])
)
nat_gw_route = aws.ec2.Route(
    "nat-gw-route",
    route_table_id=private_route_table.id,
    nat_gateway_id=nat_gw.id,
    destination_cidr_block="0.0.0.0/0"
)
public_igw_route = aws.ec2.Route(
    "public-igw-route",
    route_table_id=public_route_table.id,
    gateway_id=igw.id,
    destination_cidr_block="0.0.0.0/0"
)
pulumi.export("vpc_id", ml_vpc.id)
pulumi.export("public_subnet_1_id", public_subnet_1.id)
pulumi.export("public_subnet_2_id", public_subnet_2.id)
pulumi.export("private_subnet_1_id", private_subnet_1.id)
pulumi.export("private_subnet_2_id", private_subnet_2.id)
