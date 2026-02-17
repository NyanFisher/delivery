package libs.errs;

public class DomainInvariantException extends RuntimeException {
    public DomainInvariantException(Error error) {
        super("Domain invariant violated: " + error.getMessage());
    }
}