output "rds_endpoint" {
  value = aws_db_instance.postgres.endpoint
}

output "redis_endpoint" {
  value = aws_elasticache_cluster.redis.cache_nodes[0].address
}

output "ecr_repository_urls" {
  value = {
    user_service    = aws_ecr_repository.user_service.repository_url
    ml_service      = aws_ecr_repository.ml_service.repository_url
    llm_agent       = aws_ecr_repository.llm_agent.repository_url
    scraper_service = aws_ecr_repository.scraper_service.repository_url
    frontend        = aws_ecr_repository.frontend.repository_url
  }
}

output "vpc_id" {
  value = aws_vpc.main.id
}

output "public_subnet_ids" {
  value = [aws_subnet.public_1.id, aws_subnet.public_2.id]
}

output "ecs_cluster_name" {
  value = aws_ecs_cluster.main.name
}