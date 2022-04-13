from composites.consumer import MessageBusConsumer
if __name__ == '__main__':
    MessageBusConsumer.declare_scheme()
    MessageBusConsumer.consumer.run()