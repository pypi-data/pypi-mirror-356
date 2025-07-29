from astrodynx.twobody.kepler_equation import (
    mean_anomaly_ecliptic,
    mean_anomaly_hyperbolic,
)

import jax.numpy as jnp


class TestMeanAnomalyEcliptic:
    def test_scalar(self) -> None:
        # Example from docstring
        e = 0.1
        E = jnp.pi / 4
        expected = E - e * jnp.sin(E)
        result = mean_anomaly_ecliptic(e, E)
        assert jnp.allclose(result, expected)

    def test_zero_eccentricity(self) -> None:
        # If eccentricity is zero, mean anomaly equals eccentric anomaly
        e = 0.0
        E = jnp.linspace(0, 2 * jnp.pi, 5)
        result = mean_anomaly_ecliptic(e, E)
        assert jnp.allclose(result, E)

    def test_array_input(self) -> None:
        # Test with array inputs
        e = jnp.array([0.0, 0.1, 0.2])
        E = jnp.array([0.0, jnp.pi / 2, jnp.pi])
        expected = E - e * jnp.sin(E)
        result = mean_anomaly_ecliptic(e, E)
        assert jnp.allclose(result, expected)

    def test_negative_eccentricity(self) -> None:
        # Negative eccentricity is non-physical but should still compute
        e = -0.1
        E = jnp.pi / 3
        expected = E - e * jnp.sin(E)
        result = mean_anomaly_ecliptic(e, E)
        assert jnp.allclose(result, expected)

    def test_types(self) -> None:
        # Test with python floats and numpy floats
        e = 0.25
        E = 1.2
        result = mean_anomaly_ecliptic(e, E)
        expected = E - e * jnp.sin(E)
        assert jnp.allclose(result, expected)


class TestMeanAnomalyHyperbolic:
    def test_scalar(self) -> None:
        # Example from docstring
        e = 1.1
        H = jnp.pi / 4
        expected = e * jnp.sinh(H) - H
        result = mean_anomaly_hyperbolic(e, H)
        assert jnp.allclose(result, expected)

    def test_array_input(self) -> None:
        # Test with array inputs
        e = jnp.array([1.1, 2.0, 3.0])
        H = jnp.array([0.0, 1.0, 2.0])
        expected = e * jnp.sinh(H) - H
        result = mean_anomaly_hyperbolic(e, H)
        assert jnp.allclose(result, expected)

    def test_zero_hyperbolic_anomaly(self) -> None:
        # If H is zero, mean anomaly is -H = 0
        e = 2.0
        H = 0.0
        expected = e * jnp.sinh(H) - H
        result = mean_anomaly_hyperbolic(e, H)
        assert jnp.allclose(result, expected)

    def test_negative_hyperbolic_anomaly(self) -> None:
        # Should handle negative H
        e = 1.5
        H = -1.0
        expected = e * jnp.sinh(H) - H
        result = mean_anomaly_hyperbolic(e, H)
        assert jnp.allclose(result, expected)

    def test_types(self) -> None:
        # Test with python floats and numpy floats
        e = 2.5
        H = 1.2
        expected = e * jnp.sinh(H) - H
        result = mean_anomaly_hyperbolic(e, H)
        assert jnp.allclose(result, expected)
