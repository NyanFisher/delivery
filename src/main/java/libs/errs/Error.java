package libs.errs;

import java.util.Objects;

public final class Error {

    private static final String SEPARATOR = "||";

    private final String code;
    private final String message;

    private Error(String code, String message) {
        this.code = code;
        this.message = message;
    }

    public static Error of(String code, String message) {
        Objects.requireNonNull(code);
        Objects.requireNonNull(message);
        return new Error(code, message);
    }

    public String getCode() {
        return code;
    }

    public String getMessage() {
        return message;
    }

    public String serialize() {
        return code + SEPARATOR + message;
    }

    public static Error deserialize(String serialized) {
        if ("A non-empty request body is required.".equals(serialized)) {
            return GeneralErrors.valueIsRequired("serialized");
        }

        String[] parts = serialized.split("\\|\\|");

        if (parts.length < 2) {
            throw new IllegalArgumentException("Invalid error serialization: '" + serialized + "'");
        }

        return new Error(parts[0], parts[1]);
    }

    /**
     * Бросает DomainInvariantException.
     * Используется в местах, где ошибка невозможна по контракту.
     */
//    public void throwException() {
//        throw new DomainInvariantException(this);
//    }

    public static void throwIf(Error error) {
        if (error != null)
            throw new DomainInvariantException(error);
    }

    @Override
    public boolean equals(Object o) {
        if (this == o)
            return true;
        if (!(o instanceof Error error))
            return false;
        return Objects.equals(code, error.code) && Objects.equals(message, error.message);
    }

    @Override
    public int hashCode() {
        return Objects.hash(code, message);
    }

    @Override
    public String toString() {
        return "Error{" + "code='" + code + '\'' + ", message='" + message + '\'' + '}';
    }
}