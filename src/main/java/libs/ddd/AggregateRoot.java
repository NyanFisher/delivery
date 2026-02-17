package libs.ddd;

import java.util.List;

public interface AggregateRoot<ID> {
    ID getId();

    List<DomainEvent> getDomainEvents();

    void clearDomainEvents();
}