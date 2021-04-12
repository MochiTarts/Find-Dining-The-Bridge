import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, FormArray, Validators } from '@angular/forms';
import { cuisinesStr } from '../../_constants/cuisines';
import { pricepointsObj } from '../../_constants/pricepoints';
import { servicesStr } from '../../_constants/services';
import { paymentsStr } from '../../_constants/payment_methods';
import { Title } from '@angular/platform-browser';
import { restaurantValidator } from '../../_validation/restaurantValidator';
import { formValidator } from '../../_validation/formValidator';
import { draftValidator } from '../../_validation/draftValidator';
import { TokenStorageService } from '../../_services/token-storage.service';
import { Router } from '@angular/router';
import { RestaurantService } from '../../_services/restaurant.service';
import { Observable } from 'rxjs';
import { formValidation } from '../../_validation/forms';
import { AuthService } from 'src/app/_services/auth.service';
import { UserService } from 'src/app/_services/user.service';
import { faEdit } from '@fortawesome/free-solid-svg-icons';
import { MediaService } from '../../_services/media.service';

@Component({
  selector: 'app-restaurant-setup',
  templateUrl: './restaurant-setup.component.html',
  styleUrls: ['./restaurant-setup.component.scss']
})
export class RestaurantSetupComponent implements OnInit {
  // role: string = '';
  email: string = '';
  userId: string = '';
  profileId: string = '';
  restaurantDetails: any;

  cuisineItems: any = [];
  serviceItems: any = [];
  paymentItems: any = [];
  pricepoints: any = [];
  resOwnerNames: any = [];

  uploadForm: FormGroup;
  validator: formValidator = new restaurantValidator();
  draftValidator: formValidator = new draftValidator();
  newImage: boolean = false;

  faEdit = faEdit;

  constructor(
    private tokenStorage: TokenStorageService,
    private formBuilder: FormBuilder,
    private titleService: Title,
    private router: Router,
    private restaurantService: RestaurantService,
    private authService: AuthService,
    private userService: UserService,
    private mediaService: MediaService,
  ) { }

  ngOnInit(): void {
    if (this.authService.isLoggedIn) {
      const user = this.tokenStorage.getUser();
      // this.role = user.role;
      this.email = user.email;
      this.userId = user.user_id;
      this.profileId = user.profile_id;
    }

    this.uploadForm = this.formBuilder.group({
      file: [''],
      owner_names: this.formBuilder.array([]),
      cuisines: [[]],
      payments: [[]],
      services: [[]],
      terms: ['', Validators.requiredTrue],
    });

    if (this.profileId) {
      this.titleService.setTitle("Edit Restaurant Profile | Find Dining Scarborough");
      var draft_btn = document.getElementById('draft-btn');
      var submit_btn = document.getElementById('submit-btn');
      draft_btn.classList.remove('col-md-6');
      submit_btn.classList.remove('col-md-6');
      draft_btn.classList.add('col-md-4');
      submit_btn.classList.add('col-md-4');

      this.restaurantService.getPendingRestaurant().subscribe((data) => {
        this.restaurantDetails = data;
        if (String(this.restaurantDetails.phone) == '1234567890')
          this.restaurantDetails.phone = '';
        this.uploadForm.get('cuisines').setValue(data.cuisines[0] ? data.cuisines : []);
        this.uploadForm.get('payments').setValue(data.payment_methods[0] ? data.payment_methods : []);
        this.uploadForm.get('services').setValue(data.offer_options[0] ? data.offer_options : []);
        this.setOwnerNames();
        for (let name of this.resOwnerNames) {
          this.ownerNames.push(this.formBuilder.group(name));
        }
      })
    }
    else {
      this.titleService.setTitle("Initial Set Up | Find Dining Scarborough");
    }

    this.pricepoints = pricepointsObj
    // dropdown
    this.cuisineItems = cuisinesStr;
    this.serviceItems = servicesStr;
    this.paymentItems = paymentsStr;
  }

  get ownerNames() {
    return this.uploadForm.get('owner_names') as FormArray;
  }

  addOwner() {
    this.ownerNames.push(this.formBuilder.group({ first_name: '', last_name: '', preferred_name: '' }));
  }

  deleteOwner(index) {
    this.ownerNames.removeAt(index);
  }

  setOwnerNames() {
    for (let i = 1; i < this.restaurantDetails.owner_first_name.length; i++) {
      this.resOwnerNames.push({
        first_name: this.restaurantDetails.owner_first_name[i],
        last_name: this.restaurantDetails.owner_last_name[i],
        preferred_name: this.restaurantDetails.owner_preferred_name[i],
      })
    }
  }

  getPricepoint() {
    let price = String(this.restaurantDetails.pricepoint);
    for (let p of this.pricepoints) {
      if (p["value"] == price) {
        return p["key"];
      }
    }
  }

  onFileSelect(event) {
    if (event.target.files.length > 0) {
      this.newImage = true;
      const file = event.target.files[0];
      this.uploadForm.get('file').setValue(file);
    }
  }

  onSubmit(option) {
    const formData = new FormData();
    formData.append('media_file', this.uploadForm.get('file').value);
    return this.mediaService.uploadRestaurantMedia(formData, 'IMAGE', 'logo_url', option.includes('SUBMIT') ? 'True' : 'False');
    // this.newImage = false;
  }

  getAnswer() {
    // Extract form inputs from the user
    let price = (<HTMLInputElement>document.getElementById('pricepoint')).value;
    let pricepoint;
    for (let p of this.pricepoints) {
      if (p["key"] == price) {
        pricepoint = p["value"];
      }
    }

    let owner_first_name = [];
    owner_first_name.push((<HTMLInputElement>document.getElementById('owner-first-name')).value);

    let owner_last_name = [];
    owner_last_name.push((<HTMLInputElement>document.getElementById('owner-last-name')).value);

    let owner_preferred_name = [];
    owner_preferred_name.push((<HTMLInputElement>document.getElementById('owner-preferred-name')).value);

    for (let name of this.ownerNames.value) {
      owner_first_name.push(name.first_name);
      owner_last_name.push(name.last_name);
      owner_preferred_name.push(name.preferred_name);
    }

    var restaurantInfo = {
      name: (<HTMLInputElement>document.getElementById('restaurant-name')).value,
      years: <any>(<HTMLInputElement>document.getElementById('years-in-business')).value,
      address: (<HTMLInputElement>document.getElementById('restaurant-address')).value,
      streetAddress2: (<HTMLInputElement>document.getElementById('StreetAdd2')).value,
      streetAddress3: (<HTMLInputElement>document.getElementById('StreetAdd3')).value,
      postalCode: (<HTMLInputElement>document.getElementById('PostalCode')).value,

      phone: <any>(<HTMLInputElement>document.getElementById('phone-number')).value,
      email: (<HTMLInputElement>document.getElementById('restaurant-email')).value,
      pricepoint: pricepoint,
      cuisines: this.uploadForm.get('cuisines').value,

      // idToken: this.idToken,

      // General Services
      offer_options: this.uploadForm.get('services').value,

      owner_first_name: owner_first_name,
      owner_last_name: owner_last_name,
      owner_preferred_name: owner_preferred_name,

      deliveryDetails: (<HTMLInputElement>document.getElementById('delivery-details')).value,
      dineinPickupDetails: (<HTMLInputElement>document.getElementById('dinein-pickup-details')).value,
      locationNotes: (<HTMLInputElement>document.getElementById('location-notes')).value,

      bio: (<HTMLInputElement>document.getElementById('restaurant-bio')).value,
      web_url: (<HTMLInputElement>document.getElementById('web_url')).value,
      facebook: (<HTMLInputElement>document.getElementById('facebook')).value,
      twitter: (<HTMLInputElement>document.getElementById('twitter')).value,
      instagram: (<HTMLInputElement>document.getElementById('instagram')).value,
      open_hours: (<HTMLInputElement>document.getElementById('open_hours')).value,
      payment_methods: this.uploadForm.get('payments').value,
    };

    return restaurantInfo;
  }

  getAnswerForProfanityCheck(restaurantInfo) {
    let newRestaurantInfo = Object.assign({}, restaurantInfo);
    newRestaurantInfo['name_p'] = restaurantInfo.name;
    newRestaurantInfo['owner_first_name_p'] = String(restaurantInfo.owner_first_name);
    newRestaurantInfo['owner_last_name_p'] = String(restaurantInfo.owner_last_name);
    newRestaurantInfo['owner_preferred_name_p'] = String(restaurantInfo.owner_preferred_name);
    newRestaurantInfo['address_p'] = restaurantInfo.address;
    newRestaurantInfo['streetAddress2_p'] = restaurantInfo.streetAddress2;
    newRestaurantInfo['streetAddress3_p'] = restaurantInfo.streetAddress3;
    newRestaurantInfo['deliveryDetails_p'] = restaurantInfo.deliveryDetails;
    newRestaurantInfo['dineinPickupDetails_p'] = restaurantInfo.dineinPickupDetails;
    newRestaurantInfo['locationNotes_p'] = restaurantInfo.locationNotes;
    newRestaurantInfo['bio_p'] = restaurantInfo.bio;
    newRestaurantInfo['open_hours_p'] = restaurantInfo.open_hours;
    return newRestaurantInfo;
  }

  chooseAPI(option: string, restaurantInfo: Object): Observable<any> {
    switch (option) {
      case 'SETUP-DRAFT':
        return this.restaurantService.insertRestaurantDraft(restaurantInfo);
      case 'SETUP-SUBMIT':
        return this.restaurantService.insertRestaurantApproval(restaurantInfo);
      case 'EDIT-DRAFT':
        return this.restaurantService.updateRestaurantDraft(restaurantInfo);
      case 'EDIT-SUBMIT':
        return this.restaurantService.insertRestaurantApproval(restaurantInfo);
      default:
        alert("Something wrong happened");
    }
  }

  chooseValidator(option: string) {
    switch (option) {
      case 'SETUP-DRAFT':
        return this.draftValidator;
      case 'SETUP-SUBMIT':
        return this.validator;
      case 'EDIT-DRAFT':
        return this.draftValidator;
      case 'EDIT-SUBMIT':
        return this.validator;
      default:
        alert("Something wrong happened");
    }
  }

  chooseAlert(option: string) {
    if (option.includes('DRAFT')) {
      alert("Changes to restaurant are now saved as draft");
    } else {
      alert("Changes to restaurant are now pending admin approval");
    }
  }

  improveDraftAnswer(restaurantInfo) {
    if (!restaurantInfo.years) {
      restaurantInfo.years = "0";
    }
    if (!restaurantInfo.phone) {
      restaurantInfo.phone = "1234567890";
    }
    return restaurantInfo;
  }

  typeConversion(restaurantInfo) {
    // Convert type of fields to match with backend
    restaurantInfo.years = Number(restaurantInfo.years);
    restaurantInfo.phone = Number(restaurantInfo.phone);
    if (restaurantInfo.offer_options.length == 0) {
      restaurantInfo.offer_options.push('');
    }
    if (restaurantInfo.payment_methods.length == 0) {
      restaurantInfo.payment_methods.push('');
    }
    return restaurantInfo;
  }

  setupROProfile(option: string) {

    let restaurantInfo = this.getAnswer();

    if (option.includes('DRAFT')) {
      restaurantInfo = this.improveDraftAnswer(restaurantInfo);
    }

    let restaurantInfoForProfanityCheck = this.getAnswerForProfanityCheck(restaurantInfo);

    let validator = this.chooseValidator(option);
    this.validator.clearAllErrors();
    let failFlag = validator.validateAll(restaurantInfoForProfanityCheck, (key) => {
      this.validator.setError(key);
    });

    if (!failFlag) {
      if (option.includes('SUBMIT') && !window.confirm('Are you sure you want to submit?')) {
        return;
      } else if (option.includes('DRAFT') && !window.confirm('Are you sure you want to save as draft?')) {
        return;
      }

      restaurantInfo = this.typeConversion(restaurantInfo);

      // Select which api to call depending on option
      this.chooseAPI(option, restaurantInfo).subscribe((data) => {
        if (data && formValidation.isInvalidResponse(data)){
          formValidation.HandleInvalid(data, (key) => this.validator.setError(key))
        } else {

          if (option.includes('SETUP')) {
            let roInfo = {
              restaurant_id: data._id,
            };
            this.restaurantService.roSignup(roInfo).subscribe((profile) => {
              var sduserInfo = {
                profile_id: profile.id,
              };
              this.userService.editAccountUser(sduserInfo).subscribe(() => {
                this.authService.refreshToken().subscribe((token) => {
                  if (this.newImage) {
                    this.onSubmit(option).subscribe(() => {
                      this.newImage = false;
                    })
                  }
                  this.tokenStorage.updateTokenAndUser(token.access);
                  this.router.navigate(['/restaurant']).then(() => {
                    this.chooseAlert(option);
                    this.reload();
                  });
                });
              });
            });

          } else {
            if (this.newImage) {
              this.onSubmit(option).subscribe(() => {
                this.newImage = false;
              })
            }
            this.router.navigate(['/restaurant']).then(() => {
              this.chooseAlert(option);
              this.reload();
            });
          }

        }
      });


    } else {
      window.scrollTo(0, 0);
      alert("Please ensure all fields are entered in correctly")
    }
  }

  reload() {
    this.authService.refreshToken().subscribe((token) => {
      this.tokenStorage.updateTokenAndUser(token.access);
      let currentUrl = this.router.url;
      this.router.routeReuseStrategy.shouldReuseRoute = () => false;
      this.router.onSameUrlNavigation = 'reload';
      this.router.navigate([currentUrl]);
    });
  }

  cancel() {
    if (!window.confirm('Are you sure you want to navigate away? Any unsubmitted changes will be lost.')) {
      return;
    }
    this.router.navigate(['/restaurant']);
  }

  gotoEditPosts() {
    this.router.navigate(['/edit-posts']);
  }

  updateCuisineList(cuisines: any[]) {
    this.uploadForm.get('cuisines').setValue(cuisines);
  }

  updatePaymentList(payments: any[]) {
    this.uploadForm.get('payments').setValue(payments);
  }

  updateServiceList(services: any[]) {
    this.uploadForm.get('services').setValue(services);
  }

}
