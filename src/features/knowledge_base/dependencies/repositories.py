import logging
import os
from src.di.container import Container
from src.di.domain.exceptions import DependencyNotRegistered
from src.features.knowledge_base.infrastructure.sqlalchemy.knowledge_repository import SqlAlchemyKnowledgeRepository
from src.persistence.domain import data_repository, file_repository
from src.persistence.infrastructure.boto3.file_repository import Boto3FileRepository
logger = logging.getLogger(__name__)

def get_knowledge_data_repository() -> data_repository.DataRepository:
    try:
        instance_key = "knowledge_data_repository",
        repository = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        repository = SqlAlchemyKnowledgeRepository()
        Container.register(instance_key, repository)
        logger.debug(f"{instance_key} registered")
    
    return repository

def get_knowledge_file_repository() -> file_repository.FileRepository:
    try:
        instance_key = "knowledge_file_repository",
        repository = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        bucket_name = os.getenv("AWS_BUCKET_NAME")
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION', 'us-east-1')
        
        if not bucket_name or not aws_access_key_id or not aws_secret_access_key:
            raise ValueError("Boto3 file reposotory variable not configured")
        
        repository = Boto3FileRepository(
            aws_secret_access_key=aws_secret_access_key,
            aws_access_key_id=aws_access_key_id,
            region_name=region_name,
            bucket_name=bucket_name
        )
        Container.register(instance_key, repository)
        logger.debug(f"{instance_key} registered")
    
    return repository