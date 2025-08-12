from abc import ABC, abstractmethod
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


class Vehicle(ABC):
    def __init__(self, make: str, model: str, spec: str) -> None:
        self.make = make
        self.model = model
        self.spec = spec

    @abstractmethod
    def start_engine(self) -> None:
        pass


class Car(Vehicle):

    def start_engine(self) -> None:
        logging.info("%s %s (%s): Двигун запущено", self.make, self.model, self.spec)


class Motorcycle(Vehicle):

    def start_engine(self) -> None:
        logging.info("%s %s (%s): Мотор заведено", self.make, self.model, self.spec)


class VehicleFactory(ABC):

    @abstractmethod
    def create_car(self, make: str, model: str) -> Car:
        pass

    @abstractmethod
    def create_motorcycle(self, make: str, model: str) -> Motorcycle:
        pass


class USVehicleFactory(VehicleFactory):

    def create_car(self, make: str, model: str) -> Car:
        car = Car(make, model, "US Spec")
        logging.info("Car %s %s (%s) has been created", make, model, "US Spec")
        return car

    def create_motorcycle(self, make: str, model: str) -> Motorcycle:
        motorcycle = Motorcycle(make, model, "US Spec")
        logging.info("Motorcycle %s %s (%s) has been created", make, model, "US Spec")
        return motorcycle


class EUVehicleFactory(VehicleFactory):

    def create_car(self, make: str, model: str) -> Car:
        car = Car(make, model, "EU Spec")
        logging.info("Car %s %s (%s) has been created", make, model, "EU Spec")
        return car

    def create_motorcycle(self, make: str, model: str) -> Motorcycle:
        motorcycle = Motorcycle(make, model, "EU Spec")
        logging.info("Motorcycle %s %s (%s) has been created", make, model, "EU Spec")
        return motorcycle


# Використання
vehicle1 = EUVehicleFactory().create_car("Toyota", "Corolla")
vehicle1.start_engine()

vehicle2 = USVehicleFactory().create_motorcycle("Harley-Davidson", "Sportster")
vehicle2.start_engine()
