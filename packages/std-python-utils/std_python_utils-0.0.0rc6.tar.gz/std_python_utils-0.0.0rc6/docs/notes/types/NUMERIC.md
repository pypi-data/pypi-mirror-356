# 🔢 Numeric ABCs & Types (`numbers`, `fractions`, `decimal`)

| Name            | Module           | Inherits From | Description |
|-----------------|------------------|-----------|-------------|
| **Number**       | `numbers`        | —         | Root ABC for all numeric types. |
| **Complex**      | `numbers`        | `Number`  | Supports real + imaginary parts. Includes built-in `complex`. |
| **Real**         | `numbers`        | `Complex` | Represents real numbers. Includes built-in `float`. |
| **Rational**     | `numbers`        | `Real`    | Has `numerator` and `denominator`. |
| **`Decimal`**    | `decimal`        | `Real`    | Decimal floating point with user-defined precision. |
| **Integral**     | `numbers`        | `Rational` | Represents whole numbers. Includes built-in `int`. |
| **`int`**        | Built-in         | `Integral` | Standard integer type. |
| **`float`**      | Built-in         | `Real`    | IEEE 754 floating point. |
| **`complex`**    | Built-in         | `Complex` | Complex number with real + imag parts. |
| **`Fraction`**   | `fractions`      | `Rational` | Exact fractional arithmetic. |
