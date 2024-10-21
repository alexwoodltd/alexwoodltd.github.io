---
title: "Contact Us"
permalink: /contact/
---

<form class="form" action="{FORM_ENDPOINT}" method="POST">
  <div class="mb-3 pt-0">
    <input type="text" placeholder="Your name" name="name" required />
  </div>
  <div class="mb-3 pt-0">
    <input type="email" placeholder="Email" name="email" required />
  </div>
  <div class="mb-3 pt-0">
    <textarea placeholder="Your message" name="message" required></textarea>
  </div>
  <div class="mb-3 pt-0">
    <button type="submit">Send</button>
  </div>
</form>