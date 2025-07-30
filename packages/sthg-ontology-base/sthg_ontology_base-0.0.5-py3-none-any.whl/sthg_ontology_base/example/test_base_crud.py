from datetime import datetime
from sthg_ontology_base.utils.base_crud import BaseModel
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
from sqlalchemy import (
    create_engine, Column, String, DateTime, Text, Boolean, INT
)
from sthg_ontology_base import FoundryClient


class OntologyModel(BaseModel):
    __tablename__ = "om_ontology"
    rid = Column(String(255), primary_key=True)
    api_name = Column(String(255))
    display_name = Column(String(255))
    description = Column(Text)
    create_uid = Column(String(255))
    ctime = Column(DateTime, default=datetime.utcnow)
    utime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class OntologyModelWrite(BaseModel):
    __tablename__ = "om_ontology_wirtecall"
    #_source_model = OntologyModel

    rid = Column(String(255), primary_key=True)
    api_name = Column(String(255))
    display_name = Column(String(255))
    description = Column(Text)
    create_uid = Column(String(255))
    is_delete = Column(Boolean, nullable=True, comment="创建者id")
    new_filed = Column(String(255), nullable=True, comment="新增字段")
    test_int = Column(INT, nullable=True, comment="新增字段")
    ctime = Column(DateTime, default=datetime.utcnow)
    utime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

def init_database():
    """初始化数据库连接"""
    password = "Dev@02891"
    encoded_password = quote_plus(password)
    SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://dev_user:{encoded_password}@192.168.1.171:9030/ontology_test_db"

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=3600,
        echo=False
    )
    session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # 配置到所有模型
    #BaseModel.set_session_factory(session_factory)
    return session_factory


def test_query(session_factory):
    """测试查询功能"""
    client = FoundryClient(session_factory)
    print("\n测试查询所有记录:")
    # results = client.ontology.objects.OntologyModelWrite.where(~OntologyModelWrite.api_name.is_null()).order_by(OntologyModelWrite.test_int.desc())
    #
    #
    # results = client.ontology.objects.OntologyModelWrite.count_all()
    results = client.ontology.objects.OntologyModelWrite.limit(5).offset(2).order_by(OntologyModelWrite.test_int)
    print(results)



def test_create(session_factory):
    """测试创建功能"""
    client = FoundryClient(session_factory)
    print("\n测试创建记录:")
    new_item = client.ontology.objects.OntologyModelWrite.create(
        rid="test_009",
        api_name="test_api9",
        display_name="测试模型39",
        create_uid="tester9"
    )
    print(f"创建成功: RID={new_item.rid}")


def test_update(session_factory):
    """测试更新功能"""
    client = FoundryClient(session_factory)
    print("\n测试更新操作:")

    # 先创建测试数据
    test_item = client.ontology.objects.OntologyModelWrite.create(
        rid="temp_001",
        api_name="temp_api",
        display_name="临时模型",
        create_uid="tester"
    )

    # 执行更新
    updated_count = client.ontology.objects.OntologyModelWrite.where(
        OntologyModelWrite.rid == "temp_001"
    ).update(display_name="已更新模型", new_filed="新增字段值")

    print(f"更新了 {updated_count} 条记录")

    # 验证更新
    result = client.ontology.objects.OntologyModelWrite.where(
        OntologyModelWrite.rid == "temp_001"
    ).first()
    print(f"更新后数据: {result.__dict__}")


def test_delete(session_factory):
    """测试删除功能"""
    client = FoundryClient(session_factory)
    print("\n测试删除操作:")

    # 先创建测试数据
    test_item = client.ontology.objects.OntologyModelWrite.create(
        rid="del_001",
        api_name="del_api",
        display_name="待删模型",
        create_uid="tester"
    )

    # 执行删除
    deleted_count = client.ontology.objects.OntologyModelWrite.where(
        OntologyModelWrite.rid == "del_001"
    ).delete()

    print(f"删除了 {deleted_count} 条记录")

    # 验证删除
    result = client.ontology.objects.OntologyModelWrite.where(
        OntologyModelWrite.rid == "del_001"
    ).first()
    print(f"删除后查询结果: {'存在' if result else '不存在'}")


if __name__ == "__main__":
    # 初始化数据库
    session_factory = init_database()

    # 执行测试套件
    test_query(session_factory)
    #test_create(session_factory)
    #test_update(session_factory)
    #test_delete(session_factory)