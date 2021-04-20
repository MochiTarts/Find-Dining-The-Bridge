import { Component, OnInit } from '@angular/core';
import { EmailService } from 'src/app/_services/email.service';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Title } from '@angular/platform-browser';

@Component({
  selector: 'app-contact-us',
  templateUrl: './contact-us.component.html',
  styleUrls: ['./contact-us.component.scss']
})
export class ContactUsComponent implements OnInit {
  messageForm: FormGroup;

  constructor(
    private emailService: EmailService,
    private formBuilder: FormBuilder,
    private titleService: Title,
  ) { }

  ngOnInit(): void {
    this.titleService.setTitle("Contact Us | Find Dining Scarborough");

    this.messageForm = this.formBuilder.group({
      name: ['', Validators.required],
      email: ['', [Validators.email, Validators.required]],
      message: ['', Validators.required],
    });
  }

  /**
   * Performs action to send email to info@finddining.ca
   */
  onSubmit(): void {
    let name = this.messageForm.get('name').value;
    let message = this.messageForm.get('message').value;
    let content = "<p>Email from:" + this.messageForm.get('email').value + "</p><p>Name: " + name + "</p><p>Message: " + message + "</p>";

    var emailInfo = {
      subject: 'Message From Landing Page',
      content
    }

    this.emailService.sendEmail(emailInfo).subscribe((data) => {
      alert("Your message is submitted!");
      window.location.reload();
    },
      err => {
        alert(err.error.message);
      });
  }

}
