package libs.errs;

public final class GeneralErrors {

    private GeneralErrors() {
        // Utility class, no instantiation
    }

    public static <T> Error notFound(String name, T id) {
        if (isNullOrEmpty(name)) {
            throw new IllegalArgumentException("Name must not be null or empty");
        }

        return Error.of(
                "record.not.found",
                String.format("Record not found. Name: %s, id: %s", name, id)
        );
    }

    public static <T> Error valueIsInvalid(String name, T value) {
        if (isNullOrEmpty(name)) {
            throw new IllegalArgumentException("Name must not be null or empty");
        }

        return Error.of(
                "value.is.invalid",
                String.format("Value '%s' is invalid for %s", value, name)
        );
    }

    public static Error valueIsRequired(String name) {
        if (isNullOrEmpty(name)) {
            throw new IllegalArgumentException("Name must not be null or empty");
        }
        return Error.of("value.is.required", "Value is required for " + name);
    }

    public static Error invalidLength(String name) {
        if (isNullOrEmpty(name)) {
            throw new IllegalArgumentException("Name must not be null or empty");
        }
        return Error.of("invalid.string.length", "Invalid " + name + " length");
    }

    public static Error collectionIsTooSmall(int min, int current) {
        return Error.of("collection.is.too.small",
                "The collection must contain " + min + " items or more. It contains " + current + " items.");
    }

    public static Error collectionIsTooLarge(int max, int current) {
        return Error.of("collection.is.too.large",
                "The collection must contain " + max + " items or fewer. It contains " + current + " items.");
    }

    public static <T extends Comparable<T>> Error valueIsOutOfRange(String name, T value, T min, T max) {
        if (isNullOrEmpty(name)) {
            throw new IllegalArgumentException("Name must not be null or empty");
        }

        String message = String.format("Value %s for %s is out of range. Min value is %s, max value is %s.", value,
                name, min, max);

        return Error.of("value.is.out.of.range", message);
    }

    public static <T extends Comparable<T>> Error valueMustBeGreaterThan(
            String name,
            T value,
            T min) {

        if (isNullOrEmpty(name)) {
            throw new IllegalArgumentException("Name must not be null or empty");
        }

        return Error.of(
                "value.must.be.greater.than",
                String.format(
                        "The value of %s (%s) must be greater than %s.",
                        name,
                        value,
                        min
                )
        );
    }

    public static <T extends Comparable<T>> Error valueMustBeGreaterOrEqual(
            String name,
            T value,
            T min) {

        if (isNullOrEmpty(name)) {
            throw new IllegalArgumentException("Name must not be null or empty");
        }

        return Error.of(
                "value.must.be.greater.or.equal",
                String.format(
                        "The value of %s (%s) must be greater than or equal to %s.",
                        name,
                        value,
                        min
                )
        );
    }

    public static <T extends Comparable<T>> Error valueMustBeLessThan(
            String name,
            T value,
            T max) {

        if (isNullOrEmpty(name)) {
            throw new IllegalArgumentException("Name must not be null or empty");
        }

        return Error.of(
                "value.must.be.less.than",
                String.format(
                        "The value of %s (%s) must be less than %s.",
                        name,
                        value,
                        max
                )
        );
    }

    public static <T extends Comparable<T>> Error valueMustBeLessOrEqual(
            String name,
            T value,
            T max) {

        if (isNullOrEmpty(name)) {
            throw new IllegalArgumentException("Name must not be null or empty");
        }

        return Error.of(
                "value.must.be.less.or.equal",
                String.format(
                        "The value of %s (%s) must be less than or equal to %s.",
                        name,
                        value,
                        max
                )
        );
    }

    private static boolean isNullOrEmpty(String s) {
        return s == null || s.trim().isEmpty();
    }
}
