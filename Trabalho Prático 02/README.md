# Localização de UPAs

## Descrição
Existem n distritos numa região metropolitana. A distância entre o distrito i e o distrito j é dada por dij. Deseja-se escolher em quais distritos devem ser instaladas UPAs
(Unidades de Pronto-Atendimento). A legislação obriga que a distância entre um distrito e a UPA mais próxima seja de no máximo X quilômetros e que a distância até a segunda UPA mais próxima seja no máximo de Y quilômetros. Além disso, deseja-se que a distância entre 2 UPAs não seja menor do que Z quilômetros.
A implementação funciona para qualquer conjunto de dados e fornece a resposta completa: em quais distritos foram instaladas UPAs e as distâncias de cada distrito para a primeira e a segunda UPA mais próxima.

A distância em km entre os distritos i e j pode ser obtida pelas coordenadas através da fórmula:
  <p align="center">
    <img src="https://user-images.githubusercontent.com/54148100/103824427-a3c3f180-5052-11eb-8bc7-e480c5cbea6a.png" alt="Sublime's custom image"/>
  </p>
  <p align="center">
    Figura 1: Fórmula da distância.
  </p>
  
## Formato do arquivo
````
n X Y Z
x1 y1
. 
.
.
xn yn
````

- n = número de distritos
- X = valor máximo entre a 1ª UPA e o distrito
- Y = valor máximo entre a 2ª UPA e o distrito
- Z = valor mínimo entre duas UPAs
- x = valor de coordenada x do distrito
- y = valor de coordenada y do distrito

Como exemplo de teste, é utilizado o arquivo [instance.txt](https://github.com/WellyngtonMS/Pesquisa-Operacional/blob/main/Trabalho%20Pr%C3%A1tico%2002/instance.txt) disponível no repositório.

Qual é o menor número de UPAs que devem ser instaladas?
