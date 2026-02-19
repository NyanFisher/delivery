import pydantic_settings


class DBProperties(pydantic_settings.BaseSettings):
    dsn: str = "postgresql+psycopg://username:secret@localhost:5432/delivery??sslmode=disable"

    model_config = pydantic_settings.SettingsConfigDict(env_prefix="db_")


class GeoProperties(pydantic_settings.BaseSettings):
    host: str = "http://0.0.0.0"
    port: str = "5004"

    model_config = pydantic_settings.SettingsConfigDict(env_prefix="geo_")


class KafkaConsumerProperties(pydantic_settings.BaseSettings):
    group_id: str = "delivery-group"
    auto_offset_reset: str = "earliest"
    key_deserializer: str = "org.apache.kafka.common.serialization.StringDeserializer"
    value_deserializer: str = "org.apache.kafka.common.serialization.ByteArrayDeserializer"

    model_config = pydantic_settings.SettingsConfigDict(env_prefix="kafka_consumer_")


class KafkaProducerProperties(pydantic_settings.BaseSettings):
    key_deserializer: str = "org.apache.kafka.common.serialization.StringSerializer"
    value_deserializer: str = "org.apache.kafka.common.serialization.ByteArraySerializer"

    model_config = pydantic_settings.SettingsConfigDict(env_prefix="kafka_producer_")


class KafkaProperties(pydantic_settings.BaseSettings):
    bootstrap_servers: str = "http://localhost:9092"
    baskets_events_topic: str = "baskets.events"
    orders_events_topic: str = "orders.events"

    kafka_producer_properties = KafkaProducerProperties()
    kafka_consumer_properties = KafkaConsumerProperties()

    model_config = pydantic_settings.SettingsConfigDict(env_prefix="kafka_")


class ApplicationSettings(pydantic_settings):
    geo_properties = GeoProperties()
    kafka_properties = KafkaProperties()
    db_properties = DBProperties()
