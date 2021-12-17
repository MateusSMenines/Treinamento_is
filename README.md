# Treinamento_is

### Para rodar o o container do Rabbitmq use:

```
sudo docker run -d --rm -p 5672:5672 -p 15672:15672 rabbitmq:3.7.6-management
```

### Rodando o GATEWAY:

```
sudo docker run --rm --network=host mateusmenines/trabalho-is:gateway

```

### Rodando o ROBOT:

```
sudo docker run --rm --network=host mateusmenines/trabalho-is:robot
```

### Rodando o CLIENT

```
sudo docker run --rm --network=host mateusmenines/trabalho-is:client
```
