**Следующие действия актуальны для Raspbian 10.**
# Инструкция по развертыванию:
1. На Raspberry Pi установить Python 3, Tor*;
1. Установить следующие модули для Python 3:
<ol type="a">
  <li>Requests     </li>
  <li>PySocks*     </li>
  <li>Opencv-python</li>
</ol>
3. Сконфигурировать ботов. Файлы конфигурации находятся в папке bots и называются также как и файлы, содержащие классы соответствующих ботов. В файле конфигурации нужно изменить:
<ol type="a">
  <li> a.api_url: адресс api, использующийся ботом. Включает протокол (http/https);</li>
  <li> b.user_id: id пользователя, целое число;                                    </li>
  <li> c.access_token: токен доступа, строка. Для бота в Telegram получить у BotFather, для ВКонтакте - следовать инструкции с https://vkhost.github.io/ ;</li>
</ol>
4.  Сконфигурировать комнаты. Для этого следует изменить файл homeConfig.json для соответствия собранной системе. Значения hasLight и hasCamera обязательны. Если hasLight = true, следует указать lightPin - пин, к которому подключен модуль реле. Если hasCamera = true и к Raspberry Pi подключено несколько веб-камер, следует также указать cameraId.
5. Сконфигурировать Tor для работы Socks5 на порту 9150*
6. Добавить автозапуск main.py через cron

*Если Тг заблокирован в стране, где планируется использовать бота.
