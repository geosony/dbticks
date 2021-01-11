from handlers.endpoints import UploadHandler, ListHandler, TicketDetailHandler, TicketCompareHandler, TicketUpdateHandler

handlers = [
    (r'/upload', UploadHandler),
    (r'/tickets', ListHandler),
    (r'/tickets/([a-z0-9]+)/update', TicketUpdateHandler),
    (r'/tickets/([a-z0-9]+)/detail', TicketDetailHandler),
    (r'/tickets/([a-z0-9]+)/compare', TicketCompareHandler),
]
