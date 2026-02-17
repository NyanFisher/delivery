package libs.ddd;

public interface DomainEventPublisher {
    void publish(Iterable<Aggregate<?>> aggregates);
}