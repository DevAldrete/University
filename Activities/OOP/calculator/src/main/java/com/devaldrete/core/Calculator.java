package com.devaldrete.core;

public interface Calculator<T> {
  T add(T a, T b);

  T substract(T a, T b);

  T multiply(T a, T b);

  T divide(T a, T b);
}
