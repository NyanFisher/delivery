package libs.ddd;

import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Getter;
import org.springframework.context.ApplicationEvent;

import java.time.Instant;
import java.util.UUID;

@Getter
public abstract class DomainEvent extends ApplicationEvent {
    private final UUID eventId = UUID.randomUUID();
    private final Instant occurredOnUtc = Instant.now();

    public DomainEvent(Object source) {
        super(source);
    }

    // Fake Ctr for Jackson / JPA
    protected DomainEvent() {
        super("default");
    }

    @JsonIgnore
    @Override
    public Object getSource() {
        return super.getSource();
    }
}