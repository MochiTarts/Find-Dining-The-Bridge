import { Component, OnInit } from '@angular/core';
import { Title } from '@angular/platform-browser';
import {
  faMapMarkerAlt,
  faPhone,
  faEdit,
  faShippingFast,
  faShareAlt
} from '@fortawesome/free-solid-svg-icons';
import { faHeart, faEnvelope } from '@fortawesome/free-regular-svg-icons';
import { faTwitter, faInstagram, faFacebookF } from '@fortawesome/free-brands-svg-icons';
import { ActivatedRoute, Router } from '@angular/router';
import { FormBuilder, FormGroup } from '@angular/forms';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { linkValidator } from '../../_validation/linkValidator';
import { formValidator } from 'src/app/_validation/formValidator';
import getVideoId from 'get-video-id';
import { AuthService } from 'src/app/_services/auth.service';
import { TokenStorageService } from '../../_services/token-storage.service';
import { RestaurantService } from '../../_services/restaurant.service';
import { MediaService } from '../../_services/media.service';
import { Observable } from 'rxjs';
import { formValidation } from '../../_validation/forms';
import { UserService } from '../../_services/user.service';

@Component({
  selector: 'app-restaurant-page',
  templateUrl: './restaurant-page.component.html',
  styleUrls: ['./restaurant-page.component.scss']
})
export class RestaurantPageComponent implements OnInit {
  restaurantId: string = '';
  role: string = '';
  email: string = '';
  userId: string = '';
  profileId: string = '';

  error: boolean = false;

  restaurantDetails: any;
  restaurantMenu: any[] = [];
  categories: string[] = [];
  specialDish: any[] = [];
  popularDish: any[] = [];

  pricepoints: any = [];
  pricepoint: string = '';
  displayed_phone: string = '';
  cuisineList: string = '';
  serviceList: string = '';
  paymentList: string = '';

  firstFourServices: string = '';
  serviceCount = 0;
  expandService: boolean = false;

  nearbyRestaurants: any[] = [];
  isQueryRestaurant: boolean = false;

  modalRef: any;

  uploadStoryImgForm: FormGroup;
  uploadVideoForm: FormGroup;
  uploadImageForm: FormGroup;

  newFile: boolean = false;

  videoId:string = '';
  validator: formValidator = new linkValidator();
  apiLoaded = false;
  uploadMethod: string = '';
  submitVideoAllowed: boolean = false;

  imageUrls = [];
  imageUrlsToDelete = [];
  addOrRemove: string = '';
  submitImageAllowed: boolean = false;

  faMapMarker = faMapMarkerAlt;
  faPhone = faPhone;
  faMail = faEnvelope;
  faHeartLine = faHeart;
  faTwitter = faTwitter;
  faInstagram = faInstagram;
  faFacebookF = faFacebookF;
  faShareAlt = faShareAlt;
  faEdit = faEdit;
  faShippingFast = faShippingFast;

  slides = [];

  constructor(
    private titleService: Title,
    private router: Router,
    private modalService: NgbModal,
    private formBuilder: FormBuilder,
    private authService: AuthService,
    private tokenStorage: TokenStorageService,
    private restaurantService: RestaurantService,
    private route: ActivatedRoute,
    private mediaService: MediaService,
    private userService: UserService,
  ) { }

  ngOnInit(): void {
    this.titleService.setTitle("Restaurant Page | Find Dining Scarborough");

    this.pricepoints = [
      {key: "$", value: "LOW"},
      {key: "$$", value: "MID"},
      {key: "$$$", value: "HIGH"},
      {key: "$$$$", value: "EXHIGH"}
    ]

    if (this.authService.isLoggedIn) {
      const user = this.tokenStorage.getUser();
      this.role = user.role;
      this.email = user.email;
      this.userId = user.user_id;
      this.profileId = user.profile_id;
    }

    if (this.userId != null && (this.role == 'BU' || this.role == 'RO')) {
      this.getNearbyRestaurants();
    }

    this.restaurantId = this.route.snapshot.queryParams.restaurantId;

    if (this.restaurantId == this.route.snapshot.queryParams.restaurantId) this.isQueryRestaurant = true;

    this.getPendingOrApprovedRestaurant(this.restaurantId).subscribe((data) => {
      this.restaurantDetails = data;

      // tab title
      this.titleService.setTitle(data.name + " | Find Dining Scarborough");

      // displayed phone
      var phone: string = String(this.restaurantDetails.phone);
      this.displayed_phone = phone != 'null' ? "(" + phone.slice(0,3) + ") " + phone.slice(3,6) + " " + phone.slice(6,10) : '';

      // pricepoint
      let price = String(this.restaurantDetails.pricepoint);
      this.pricepoint = this.getPricepoint(price);

      // cuisine list
      for (let cus of this.restaurantDetails.cuisines) {
        if (this.cuisineList == '') {
          this.cuisineList = String(cus);
        } else {
          this.cuisineList = this.cuisineList + ", " + String(cus);
        }
      }

      // service list
      for (let service of this.restaurantDetails.offer_options) {
        if (this.serviceList == '') {
          this.serviceList = String(service);
          this.firstFourServices = this.serviceList;
          this.serviceCount += 1;
        } else {
          this.serviceList = this.serviceList + " | " + String(service);
          if(this.serviceCount < 4) {
            this.firstFourServices = this.serviceList;
          }
          this.serviceCount += 1;
        }
      }

      // payment list
      this.paymentList = this.restaurantDetails.payment_methods.toString().split(',').join(', ') + " Accepted";

      this.uploadStoryImgForm = this.formBuilder.group({
        file: [''],
      });

      this.uploadVideoForm = this.formBuilder.group({
        file: [''],
        upload_method: ['Choose a method to upload video...'],
      });

      this.uploadImageForm = this.formBuilder.group({
        file: [''],
        add_or_remove: ['Choose a method to modify images...'],
      });

      for (let url of this.restaurantDetails.restaurant_image_url) {
        this.slides.push({url: url.replace(' ', '%20')});
      }

      this.videoId = this.getVideoId(this.restaurantDetails.restaurant_video_url);
    }, (error) => {
      this.error = true;
    });

    this.getPendingOrApprovedDishes(this.restaurantId).subscribe((data) => {
      this.restaurantMenu = data.Dishes;
      for (let dish of data.Dishes) {
        if (dish.category == "Popular Dish") {
          this.popularDish.push(dish)
        } else if (dish.category == "Special") {
          this.specialDish.push(dish);
        }
      }
    }, (error) => {
      this.error = true;
    });

    if (!this.apiLoaded) {
      // This code loads the IFrame Player API code asynchronously, according to the instructions at
      // https://developers.google.com/youtube/iframe_api_reference#Getting_Started
      const tag = document.createElement('script');
      tag.src = 'https://www.youtube.com/iframe_api';
      document.body.appendChild(tag);
      this.apiLoaded = true;
    }

  }

  getPendingOrApprovedRestaurant(id) {
    if (this.authService.isLoggedIn && this.role == 'RO' && !this.isQueryRestaurant) {
      return this.restaurantService.getPendingRestaurant();
    } else {
      return this.restaurantService.getApprovedRestaurant(id);
    }
  }

  getPendingOrApprovedDishes(id) {
    if (this.authService.isLoggedIn && this.role == 'RO' && !this.isQueryRestaurant) {
      return this.restaurantService.getPendingRestaurantFood();
    } else {
      return this.restaurantService.getApprovedRestaurantFood(id);
    }
  }

  getPricepoint(priceLevel: string) {
    // priceLevels: LOW, MID, HIGH, EXHIGH
    // return: $, $$, $$$, $$$$
    for (let p of this.pricepoints) {
      if (p["value"] == priceLevel) {
        return p["key"];
      }
    }
  }

  editRestaurant() {
    this.router.navigate(['/restaurant-setup']);
  }

  editMenu() {
    this.router.navigate(['/menu-edit']);
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

  openEditModal(content) {
    this.modalRef = this.modalService.open(content, { size: 's' });
    this.newFile = false;
  }

  onStoryImgSelect(event) {
    if (event.target.files.length > 0) {
      const file = event.target.files[0];
      this.uploadStoryImgForm.get('file').setValue(file);
      this.newFile = true;
    }
  }

  onVideoFileSelect(event) {
    if (event.target.files.length > 0) {
      const file = event.target.files[0];
      this.uploadVideoForm.get('file').setValue(file);
      this.submitVideoAllowed = true;
    }
  }

  onImageFileSelect(event) {
    if (event.target.files.length > 0) {
      const file = event.target.files;
      this.uploadImageForm.get('file').setValue(file);
      this.newFile = true;
    }
  }

  onSubmitStoryImg() {
    const formData = new FormData();
    formData.append('media_file', this.uploadStoryImgForm.get('file').value);

    this.mediaService.uploadRestaurantMedia(formData, 'IMAGE', 'cover_photo_url', 'False').subscribe((data) => {
      this.reload();
    })
    this.modalRef.close();
  }

  onSubmitFullMenu() {
    let linkInfo = {
      full_menu_url: (<HTMLInputElement>document.getElementById('full_menu_url')).value,
    }
    this.validator.clearAllErrors();
    let failFlag = this.validator.validateAll(linkInfo, (key) => this.validator.setError(key));
    if (!failFlag) {
      this.chooseUpdateAPI(this.restaurantDetails.status, linkInfo).subscribe((data) => {
        this.modalRef.close();
        this.reload();
      }, (error) => {
        if (error.error && formValidation.isInvalidResponse(error.error)) {
          formValidation.HandleInvalid(error.error, (key) =>
            this.validator.setError(key)
          );
        }
      });
    } else {
      alert("Please ensure all fields are entered in correctly");
    }
  }

  onSubmitVideo() {
    const formData = new FormData();
    formData.append('media_type', 'VIDEO');
    formData.append('save_location', 'restaurant_video_url');
    formData.append('first_time_submission', 'False');
    if (this.uploadMethod == 'Upload .mp4 video file') {
      formData.append('media_file', this.uploadVideoForm.get('file').value);
      this.mediaService.uploadRestaurantMedia(formData, 'VIDEO', 'restaurant_video_url', 'False').subscribe((data) => {
        this.reload();
      });
      this.modalRef.close();
    } else if (this.uploadMethod == 'YouTube video link') {
      let linkInfo = {
        link: (<HTMLInputElement>document.getElementById('youtube_link')).value
      };
      this.validator.clearAllErrors();
      let failFlag = this.validator.validateAll(linkInfo, (key) => this.validator.setError(key));
      if (!failFlag) {
        formData.append('media_link', linkInfo.link);
        this.mediaService.uploadRestaurantMedia(formData, 'VIDEO', 'restaurant_video_url', 'False').subscribe((data) => {
          this.reload();
        });
        this.modalRef.close();
      }
    }
  }

  onSubmitImage() {
    const formData = new FormData();
    if (this.addOrRemove == 'Upload new images') {
      for (let i = 0; i < this.uploadImageForm.get('file').value.length; i++) {
        formData.append('media_file', this.uploadImageForm.get('file').value[i]);
      }
      this.mediaService.uploadRestaurantMedia(formData, 'IMAGE', 'restaurant_image_url', 'False').subscribe((data) => {
        this.reload();
      });
    } else if (this.addOrRemove == 'Delete from existing images') {
      formData.append('restaurant_images', JSON.stringify(this.imageUrlsToDelete));
      this.mediaService.deleteRestaurantMedia(formData).subscribe(() => {
        this.reload();
      });
    }
    this.modalRef.close();
  }

  updateUploadMethod() {
    this.uploadMethod = (<HTMLInputElement>document.getElementById('upload_method')).value;
    this.submitVideoAllowed = false;
  }

  updateAddOrRemove() {
    this.addOrRemove = (<HTMLInputElement>document.getElementById('add_or_remove')).value;
    if (this.addOrRemove == 'Delete from existing images') {
      this.imageUrls = Object.assign([], this.restaurantDetails.restaurant_image_url);
      this.imageUrlsToDelete = [];
    }
  }

  getVideoId(link: string) {
    return (getVideoId(link) as {id, service}).id;
  }

  deleteImage(imgUrl: string) {
    if (imgUrl != undefined && !this.imageUrlsToDelete.includes(imgUrl)) {
      this.imageUrlsToDelete.push(imgUrl);
      this.imageUrls.forEach((url, index) => {
        if (url == imgUrl) delete this.imageUrls[index];
      });
    }
  }

  chooseUpdateAPI(status: string, linkInfo: Object): Observable<any> {
    linkInfo['name'] = this.restaurantDetails.name;
    linkInfo['address'] = this.restaurantDetails.address;
    linkInfo['postalCode'] = this.restaurantDetails.postalCode;
    linkInfo['owner_first_name'] = this.restaurantDetails.owner_first_name;
    linkInfo['owner_last_name'] = this.restaurantDetails.owner_last_name;

    switch (status) {
      case 'In_Progress':
        return this.restaurantService.updateRestaurantDraft(linkInfo);
      default:
        linkInfo['years'] = this.restaurantDetails.years;
        linkInfo['phone'] = this.restaurantDetails.phone;
        linkInfo['pricepoint'] = this.restaurantDetails.pricepoint;
        linkInfo['bio'] = this.restaurantDetails.bio;
        linkInfo['open_hours'] = this.restaurantDetails.open_hours;
        linkInfo['payment_methods'] = this.restaurantDetails.payment_methods;
        linkInfo['offer_options'] = this.restaurantDetails.offer_options;
        return this.restaurantService.insertRestaurantApproval(linkInfo);
    }
  }

  getNearbyRestaurants() {
    this.userService.getNearbyRestaurants().subscribe((restaurants) => {
      for (let restaurant of restaurants) {
        this.restaurantService.getApprovedRestaurant(restaurant.restaurant).subscribe((data) => {
          let price = this.getPricepoint(String(data.pricepoint));
          this.nearbyRestaurants.push({
            name: data.name,
            cuisinePrice: data.cuisines[0] + " - " + price,
            imgUrl: data.logo_url,
            _id: restaurant.restaurant
          });
        })
      }
    });
  }

}
