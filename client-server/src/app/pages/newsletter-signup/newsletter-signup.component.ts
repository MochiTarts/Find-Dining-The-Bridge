import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { newsletterValidator } from '../../_validation/newsletterValidator';
import { formValidator } from '../../_validation/formValidator';
import { formValidation } from "../../_validation/forms";
import { Router } from '@angular/router';
import { Title } from '@angular/platform-browser';
import { AuthService } from '../../_services/auth.service';

@Component({
  selector: 'app-newletter-signup',
  templateUrl: './newsletter-signup.component.html',
  styleUrls: ['./newsletter-signup.component.scss']
})
export class NewsletterSignupComponent implements OnInit {
  uploadForm: FormGroup;
  validator: formValidator = new newsletterValidator();

  displayError: boolean = false;
  errorMessage: string = "";

  constructor(
    private formBuilder: FormBuilder,
    private router: Router,
    private titleService: Title,
    private authService: AuthService,
  ) { }

  ngOnInit(): void {
    this.titleService.setTitle("Newsletter Sign-up | Find Dining Scarborough");

    if (this.authService.isLoggedIn()) {
      this.router.navigate(['/newsletter']);
    }

    this.uploadForm = this.formBuilder.group({
      first_name: ['', Validators.required],
      last_name: ['', Validators.required],
      email: ['', Validators.required],
    });
  }

  onSubmit(): void {

    var userInfo = {
      first_name: (<HTMLInputElement>document.getElementById('first_name')).value,
      last_name: (<HTMLInputElement>document.getElementById('last_name')).value,
      email: (<HTMLInputElement>document.getElementById('email')).value,
      consent_status: (<HTMLInputElement>document.getElementById('receive_updates')).checked ? "EXPRESSED" : "IMPLIED",
    }

    // clear formErrors
    this.displayError = false;
    this.errorMessage = "";
    this.validator.clearAllErrors();
    let failFlag = this.validator.validateAll(userInfo, (key) =>
      this.validator.setError(key)
    );

    if (!failFlag) {
      // this.signupService.newsletterSignup(userInfo).subscribe((data) => {
      //   this.router.navigate(['/thank-you']);
      // }, (error) => {
      //   if (error.error && formValidation.isInvalidResponse(error.error)) {
      //     formValidation.HandleInvalid(error.error, (key) =>
      //       this.validator.setError(key)
      //     );
      //     this.errorMessage = "Please make sure all the information is valid!"
      //   } else {
      //     this.errorMessage = error.error.message;
      //   }
      //   this.displayError = true;
      //   this.gotoTop();
      // });
    } else {
      this.errorMessage = "Please make sure all the information is valid!"
      this.displayError = true;
      this.gotoTop();
    }

  }

  gotoTop() {
    let element = (<HTMLInputElement>document.getElementById('alert'));
    element.focus();
    window.scroll({
      top: 0,
      left: 0,
    });
  }

}
