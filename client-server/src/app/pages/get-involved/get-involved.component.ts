import { Component, OnInit, HostListener } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { EmailService } from 'src/app/_services/email.service';
import { Title } from '@angular/platform-browser';

@Component({
  selector: 'app-get-involved',
  templateUrl: './get-involved.component.html',
  styleUrls: ['./get-involved.component.scss']
})
export class GetInvolvedComponent implements OnInit {
  messageForm: FormGroup;

  arrowsOutside = true;

  partners = [
    // Example:
    // {
    //   type: 'partner',
    //   path: 'assets/images/partners/city.png',
    //   name: 'City of Toronto',
    // },
  ];

  constructor(
    private formBuilder: FormBuilder,
    private emailService: EmailService,
    private titleService: Title,
  ) { }

  ngOnInit(): void {
    this.titleService.setTitle("Get Involved | Find Dining Scarborough");
    this.messageForm = this.formBuilder.group({
      name: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      message: ['', Validators.required],
    });
  }

  @HostListener('window:resize', ['$event'])
  onResize() {
    this.arrowsOutside = window.innerWidth < 800 ? false : true;
  }

  /**
   * Performs action to send email to info@finddining.ca, asking about
   * the Get Involved activity
   */
  onSubmit(): void {
    let name = this.messageForm.get('name').value;
    let message = this.messageForm.get('message').value;
    let content = "<p>Email from:" + this.messageForm.get('email').value + "</p><p>Name: " + name + "</p><p>Message: " + message + "</p>";

    var emailInfo = {
      subject: 'Message From Get Involved Page',
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
