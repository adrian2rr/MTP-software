CC = gcc

default: libtransciever.a

libtransciever.a: methods.o commands.o utils.o constants.o spi_connector.o bcm2835.o
	ar rcs $@ $^

methods.o: methods.c methods.h
	$(CC) -c $<

commands.o: commands.c commands.h
	$(CC) -c $<

utils.o: utils.c utils.h
	$(CC) -c $<

constants.o: constants.c constants.h
	$(CC) -c $<

spi_connector.o: spi_connector.c spi_connector.h
	$(CC) -c $<

bcm2835.o: bcm2835.c bcm2835.h
	$(CC) -c $<

clean:
	rm *.o *.a
