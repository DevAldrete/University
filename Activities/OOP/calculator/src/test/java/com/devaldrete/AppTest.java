package com.devaldrete;

import junit.framework.Test;
import junit.framework.TestCase;
import junit.framework.TestSuite;
import com.devaldrete.core.SimpleCalculator;

/**
 * Unit test for simple App.
 */
public class AppTest
    extends TestCase {
  /**
   * Create the test case
   *
   * @param testName name of the test case
   */
  public AppTest(String testName) {
    super(testName);
  }

  /**
   * @return the suite of tests being tested
   */
  public static Test suite() {
    return new TestSuite(AppTest.class);
  }

  // Handy calculator tests
  public void testAddition() {
    SimpleCalculator calc = new SimpleCalculator();
    assertEquals(5, calc.add(2, 3));
    assertEquals(-1, calc.add(-2, 1));
    assertEquals(0, calc.add(0, 0));
  }

  public void testSubtraction() {
    SimpleCalculator calc = new SimpleCalculator();
    assertEquals(-1, calc.subtract(2, 3));
    assertEquals(-3, calc.subtract(-2, 1));
    assertEquals(0, calc.subtract(0, 0));
  }

  public void testMultiplication() {
    SimpleCalculator calc = new SimpleCalculator();
    assertEquals(6, calc.multiply(2, 3));
    assertEquals(-2, calc.multiply(-2, 1));
    assertEquals(0, calc.multiply(0, 100));
  }

  public void testDivision() {
    SimpleCalculator calc = new SimpleCalculator();
    assertEquals(2, calc.divide(6, 3));
    assertEquals(-2, calc.divide(-4, 2));
    try {
      calc.divide(1, 0);
      fail("Division by zero should throw an exception");
    } catch (ArithmeticException e) {
      // expected
    }
  }
}
