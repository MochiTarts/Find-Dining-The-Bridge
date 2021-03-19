import { AfterViewInit, TemplateRef } from '@angular/core';
import { ViewChild } from '@angular/core';
import { Component, OnInit } from '@angular/core';
import { FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { AuthService } from 'src/app/_services/auth.service';
import { TokenStorageService } from 'src/app/_services/token-storage.service';
import { UserService } from 'src/app/_services/user.service';
import { formValidator } from 'src/app/_validation/formValidator';
import { userValidator } from 'src/app/_validation/userValidator';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-restaurant-profile-form',
  templateUrl: './restaurant-profile-form.component.html',
  styleUrls: ['./restaurant-profile-form.component.scss']
})
export class RestaurantProfileFormComponent implements OnInit, AfterViewInit {

  @ViewChild('restaurantInfo', { static: true }) roContent: TemplateRef<any>;
  role: string = '';
  userId: string = '';
  username: string = '';
  userData: any;
  siteKey: string;
  loggedOut: boolean = true;
  formBuilder: any;

  aFormGroup: FormGroup;
  validator: formValidator = new userValidator();
  modalRef: any;
  
  constructor(
    private modalService: NgbModal,
    private router: Router,
    private authService: AuthService,
    private tokenStorageService: TokenStorageService,
    private userService: UserService
    ) { }

  ngOnInit(): void {
    if (this.authService.isLoggedIn) {
      const user = this.tokenStorageService.getUser();
      this.role = user.role;
      this.username = user.username;
      this.userId = user.email;

      this.siteKey = `${environment.captcha.siteKey}`;
      this.aFormGroup = this.formBuilder.group({
        recaptcha: ['', Validators.required],
        firstname: ['', Validators.required],
        lastname: ['', Validators.required],
        postalcode: ['', Validators.required],
        phone: ['', Validators.required],
        terms: ['', Validators.requiredTrue],
      });
    }
  }

  ngAfterViewInit(): void {
    if (this.role == 'RO') {
      this.modalRef = this.modalService.open(this.roContent, { backdrop: 'static', keyboard: false });
      /*this.userService.getConsumer({'email': this.userId}).subscribe((data) => {
        this.modalRef = this.modalService.open(this.buContent, { backdrop: 'static', keyboard: false });
      })*/
    }
  }

  reload() {
    let currentUrl = this.router.url;
    this.router.routeReuseStrategy.shouldReuseRoute = () => false;
    this.router.onSameUrlNavigation = 'reload';
    this.router.navigate([currentUrl]);
  }

  updateProfile(): void {
    var userInfo = {
      email: this.userId,
      first_name: (<HTMLInputElement>document.getElementById('firstname')).value,
      last_name: (<HTMLInputElement>document.getElementById('lastname')).value,
      postalCode: (<HTMLInputElement>document.getElementById('postalcode')).value,
      phone: <any>(<HTMLInputElement>document.getElementById('phone')).value,
      consent_status: (<HTMLInputElement>document.getElementById('casl')).checked ? "EXPRESSED" : "IMPLIED"
    };

    // clear formErrors
    this.validator.clearAllErrors();
    //validate all formfields, the callback will throw appropriate errors, return true if any validation failed
    let failFlag = this.validator.validateAll(userInfo, (key) => this.validator.setError(key));
    //if any validation failed, do not POST
    if (!failFlag) {
      userInfo.phone = Number(userInfo.phone);
      alert("Updating subscriber profile")
      this.modalRef.close();
      this.reload();
    }
  }

}