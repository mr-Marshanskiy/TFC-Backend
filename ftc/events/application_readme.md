# Модель
Application (Заявки на событие)


- **player** = **УДАЛИТЬ!**
- **event** = Событие, на которое создается заявка
- **user** = Целевой пользователь, для кого предназначена заявка
- **status** = Статус заявки.
- **comment_user** = Комментарий пользователя
- **comment_moderator** = Комментарий модератора

# Статусы
- _**1** - На модерации_
- _**2** - Принята_
- _**3** - Отклонена_
- _**4** - Приглашение ожидает ответа пользователя_
- _**5** - Отказ пользователя от участия_
- _**6** - Заявка истекла_

# Валидация

Статусы
-------

###### Создание заявки или приглашения со статусом:
- Невозможно создать заявку со статусами **Отклонена** и **Заявка истекла**

###### Изменение статуса в заявке:
- Если старый статус был **На модерации**:
  - нельзя присвоить статус **Приглашен (2)**
- Если старый статус был **Принята**:
  - можно поменять только на **Отказ пользователя от участия (5)**
- Если старый статус был **Отклонена**:
  - можно только отправить приглашение пользователю: статус **Приглашение (4)**
- Если старый статус был **Приглашен**:
  - можно только принять или отклонить приглашение. **Статусы 1, 2, 5**
- Если старый статус был **Отказ от участия**:
  - можно только отрпавить заявку на участие. **Статусы 1, 2**