package com.tutorialspoint;

public class PackageDemo {

   public static void main(String[] args) {

      // get the java lang package
      Package pack = Package.getPackage("java.lang");

      // check if this package is sealed
      System.out.println("" + pack.isSealed());
   }
}
