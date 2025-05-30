# Sistema de Emergência por Reconhecimento de Gestos

## Descrição do Problema

Em situações de emergência, pode não ser possível acessar rapidamente um telefone para pedir ajuda. Pessoas com mobilidade reduzida ou deficiência verbal enfrentam ainda mais dificuldades nesses momentos. Assim, é fundamental buscar soluções acessíveis e intuitivas que permitam acionar alertas ou pedir socorro de forma simples e eficaz através de uma câmera disponível.

---
## Grupo
- Gabriel Ciziks   | RM98215
- Lucca Tambellini | RM98169
- Cassio Valezzi   | RM551059
---

## Visão Geral da Solução

Desenvolvemos um sistema que utiliza **visão computacional e reconhecimento de gestos manuais com MediaPipe** para ativar ações de emergência:

| Gesto                      | Ação                                  |
|---------------------------|---------------------------------------|
| ✋ Mão Aberta              | Liga a lanterna (fundo branco)        |
| 🤙 Hang Loose             | Desliga a lanterna                    |
| ✊ Punho                   | Emite som de emergência (beep)        |
| ☝️ Indicador levantado    | Para o som                            |
| ✌️ Paz                    | Ativa alerta visual (mensagem em tela)|
| 🤘 Rock                   | Desativa o alerta visual              |

>  O sistema também emite mensagens faladas usando TTS (Text-To-Speech) e registra todas as ações em um arquivo de log.

---

##  Vídeo 

 [**Assista no YouTube**](https://youtu.be/exemplo_link_video)

---



##  Instruções de Uso

### 1. Criar o ambiente virtual

```
python -m venv venv
```

### 2. Ativar o ambiente virtual
```
venv\Scripts\activate
```

### 3. Instalar as dependências
```
pip install -r requirements.txt
```
### 4. Executar
```
python run.py
```