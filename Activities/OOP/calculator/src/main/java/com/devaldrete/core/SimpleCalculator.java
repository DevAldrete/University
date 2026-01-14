package com.devaldrete.core;

public class SimpleCalculator implements Calculator<Integer> {

  @Override
  public Integer add(Integer a, Integer b) {
    return a + b;
  }

  @Override
  public Integer substract(Integer a, Integer b) {
    return a - b;
  }

  @Override
  public Integer multiply(Integer a, Integer b) {
    return a * b;
  }

  @Override
  public Integer divide(Integer a, Integer b) {
    return a / b;
  }

}
