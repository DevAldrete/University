package com.devaldrete;

import java.util.Scanner;

import com.devaldrete.core.SimpleCalculator;

public class App {
  /**
   * @param args
   */
  public static void main(String[] args) {
    System.out.println("---------- Bienvenido a la Calculadora Basica ----------");
    System.out.println("Para salir de la calculadora puedes escribir 'salir'");

    try (Scanner scanner = new Scanner(System.in)) {
      while (true) {
        System.out.println("\nEscribe el primer digito: ");
        String input1 = scanner.nextLine();

        if (input1.trim().equalsIgnoreCase("salir")) {
          break;
        }

        System.out.println("Ahora, el segundo digito: ");
        String input2 = scanner.nextLine();

        if (input2.trim().equalsIgnoreCase("salir")) {
          break;
        }

        try {
          int number1 = Integer.parseInt(input1);
          int number2 = Integer.parseInt(input2);

          System.out.println("Que operacion desea realizar? (+, -, *, /)");
          String op = scanner.nextLine();

          SimpleCalculator calculator = new SimpleCalculator();

          int result;

          switch (op) {
            case "+": {
              result = calculator.add(number1, number2);
              break;
            }
            case "-": {
              result = calculator.substract(number1, number2);
              break;
            }
            case "*": {
              result = calculator.multiply(number1, number2);
              break;
            }
            case "/": {
              if (number2 == 0) {
                throw new ArithmeticException("Division no valida. Denumerador es cero.");
              }
              result = calculator.divide(number1, number2);
              break;
            }
            default: {
              System.out.println("Operacion no valida.");
              continue;
            }
          }

          System.out.printf("%d %s %d = %d\n", number1, op, number2, result);

        } catch (NumberFormatException e) {
          System.out.println("Error: Ingresa numeros validos.");
        } catch (ArithmeticException e) {
          System.out.println("Error: " + e.getMessage());
        } catch (Exception e) {
          System.out.println("Error inesperado: " + e.getMessage());
        }
      }
    }

    System.out.println("\nGracias por utilizar la calculadora.");
  }
}
