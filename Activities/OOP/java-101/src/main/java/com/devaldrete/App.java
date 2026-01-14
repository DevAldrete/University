package com.devaldrete;

import java.util.Scanner;

// My first app!
public class App {
  public static void main(String[] args) {
    Scanner entrada = new Scanner(System.in);
    int num1;
    int num2;

    System.out.println("Dame el numero 1: ");
    System.out.println("Dame el numero 2: ");

    num1 = entrada.nextInt();
    num2 = entrada.nextInt();

    int resp = num1 + num2;

    System.out.println("La suma es " + resp);

    entrada.close();
  }
}
