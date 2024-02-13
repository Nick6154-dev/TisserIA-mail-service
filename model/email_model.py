class EmailModel:
    def __init__(self, subject, sender, to, html_content, params, template_id):
        self.subject = subject
        self.sender = sender
        self.to = to
        self.html_content = html_content or ""
        self.template_id = template_id
        self.params = params or {}
