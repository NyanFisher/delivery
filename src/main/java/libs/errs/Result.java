package libs.errs;

import java.util.Objects;
import java.util.function.Consumer;
import java.util.function.Function;
public class Result<T, E extends Error> {

    private final T value;
    private final E error;
    private final boolean isSuccess;

    private Result(T value, E error, boolean isSuccess) {
        this.value = value;
        this.error = error;
        this.isSuccess = isSuccess;
    }

    /* ---------- factory ---------- */

    public static <T, E extends Error> Result<T, E> success(T value) {
        Objects.requireNonNull(value);
        return new Result<>(value, null, true);
    }

    public static <E extends Error> Result<Void, E> success() {
        return new Result<>(null, null, true);
    }

    public static <T, E extends Error> Result<T, E> failure(E error) {
        Objects.requireNonNull(error);
        return new Result<>(null, error, false);
    }

    /* ---------- state ---------- */

    public boolean isSuccess() {
        return isSuccess;
    }

    public boolean isFailure() {
        return !isSuccess;
    }

    /* ---------- access ---------- */

    public T getValue() {
        if (!isSuccess)
            throw new IllegalStateException("Cannot get value from failure");
        return value;
    }

    public E getError() {
        if (isSuccess)
            throw new IllegalStateException("Cannot get error from success");
        return error;
    }

    /* ---------- functional ---------- */

    public <U> Result<U, E> map(Function<? super T, ? extends U> mapper) {
        return isSuccess
                ? Result.success(mapper.apply(value))
                : Result.failure(error);
    }

    public <U> Result<U, E> flatMap(Function<? super T, Result<U, E>> mapper) {
        return isSuccess
                ? mapper.apply(value)
                : Result.failure(error);
    }

    public Result<T, E> onSuccess(Consumer<? super T> handler) {
        if (isSuccess) handler.accept(value);
        return this;
    }

    public Result<T, E> onFailure(Consumer<? super E> handler) {
        if (isFailure()) handler.accept(error);
        return this;
    }

    public <U> U fold(
            Function<? super T, ? extends U> onSuccess,
            Function<? super E, ? extends U> onFailure
    ) {
        return isSuccess
                ? onSuccess.apply(value)
                : onFailure.apply(error);
    }

    public <F extends Error> Result<T, F> mapError(Function<? super E, ? extends F> mapper) {
        return isSuccess
                ? Result.success(value)
                : Result.failure(mapper.apply(error));
    }

    /* ---------- fail-fast ---------- */
    /**
     * Fail-fast для домена.
     * Использовать ТОЛЬКО там, где ошибка невозможна по контракту.
     */
    public T getValueOrThrow() {
        if (isSuccess)
            return value;

        throw new DomainInvariantException(error);
    }

    @Override
    public String toString() {
        return isSuccess
                ? "Success(" + value + ")"
                : "Failure(" + error + ")";
    }
}