package libs.errs;

import java.util.Objects;
import java.util.function.Consumer;
import java.util.function.Function;

public final class UnitResult<E extends Error> {

    private final boolean isSuccess;
    private final E error;

    private UnitResult(boolean isSuccess, E error) {
        this.isSuccess = isSuccess;
        this.error = error;
    }

    /* ---------- factory ---------- */

    public static <E extends Error> UnitResult<E> success() {
        return new UnitResult<>(true, null);
    }

    public static <E extends Error> UnitResult<E> failure(E error) {
        Objects.requireNonNull(error, "Error must not be null on failure");
        return new UnitResult<>(false, error);
    }

    /* ---------- state ---------- */

    public boolean isSuccess() {
        return isSuccess;
    }

    public boolean isFailure() {
        return !isSuccess;
    }

    /* ---------- access ---------- */

    public E getError() {
        if (isSuccess)
            throw new IllegalStateException("Cannot get error from success");
        return error;
    }

    /* ---------- functional ---------- */

    public UnitResult<E> onSuccess(Runnable handler) {
        if (isSuccess) handler.run();
        return this;
    }

    public UnitResult<E> onFailure(Consumer<? super E> handler) {
        if (isFailure()) handler.accept(error);
        return this;
    }

    public <U> U fold(
            Function<Void, ? extends U> onSuccess,
            Function<? super E, ? extends U> onFailure
    ) {
        return isSuccess
                ? onSuccess.apply(null)
                : onFailure.apply(error);
    }

    /* ---------- composition ---------- */

    public UnitResult<E> merge(UnitResult<E> other) {
        if (this.isFailure()) return this;
        if (other.isFailure()) return other;
        return success();
    }

    public static <E extends Error> UnitResult<E> from(Result<Void, E> result) {
        return result.isSuccess()
                ? success()
                : failure(result.getError());
    }

    public Result<Void, E> toResult() {
        return isFailure()
                ? Result.failure(error)
                : Result.success();
    }

    /* ---------- fail-fast ---------- */

    public void getOrElseThrow(Function<? super E, ? extends RuntimeException> exceptionMapper) {
        if (isSuccess) return;
        throw exceptionMapper.apply(error);
    }

    /**
     * Fail-fast для домена.
     * Использовать ТОЛЬКО там, где ошибка невозможна по контракту.
     */
    public void getOrElseThrow() {
        if (isSuccess) return;
        throw new DomainInvariantException(error);
    }

    @Override
    public String toString() {
        return isSuccess
                ? "Success"
                : "Failure(" + error + ")";
    }
}