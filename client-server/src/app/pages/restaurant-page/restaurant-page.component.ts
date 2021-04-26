import { Component, OnInit } from '@angular/core';
import { Title } from '@angular/platform-browser';
import { Location } from '@angular/common'
import {
  faMapMarkerAlt,
  faPhone,
  faEdit,
  faShippingFast,
  faShareAlt,
  faExternalLinkAlt,
  faArrowCircleLeft,
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
import { draftValidator } from '../../_validation/draftValidator';
import { dollarPricepointsObj } from '../../_constants/pricepoints';

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

  pricepoints: any = dollarPricepointsObj;
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

  videoId: string = '';
  validator: formValidator = new linkValidator();
  draftValidator: formValidator = new draftValidator();
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
  faExternalLinkAlt = faExternalLinkAlt;
  faArrowCircleLeft = faArrowCircleLeft;

  slides = [];
  dark = "dark";

  queryParam: boolean = true;

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
    private location: Location,
  ) { }

  ngOnInit(): void {
    this.titleService.setTitle("Restaurant Page | Find Dining Scarborough");

    if (this.authService.isLoggedIn) {
      const user = this.tokenStorage.getUser();
      this.role = user.role;
      this.email = user.email;
      this.userId = user.user_id;
      this.profileId = user.profile_id;

      if (!this.route.snapshot.queryParams.restaurantId) {
        this.queryParam = false;
      }

      if (this.userId != null && this.role == 'RO'
        && !this.profileId && !this.route.snapshot.queryParams.restaurantId) {
        this.router.navigate(['/restaurant-setup']);
        return;
      }

      if (this.userId != null && (this.role == 'BU' || this.role == 'RO') && this.route.snapshot.queryParams.restaurantId) {
        this.getNearbyRestaurants();
      }
    }

    this.restaurantId = this.route.snapshot.queryParams.restaurantId;

    if (this.restaurantId) this.isQueryRestaurant = true;

    if (!this.restaurantId && !this.role) {
      this.router.navigate(['/login']);
      return;
    }

    this.getPendingOrApprovedRestaurant(this.restaurantId).subscribe((data) => {
      this.restaurantDetails = data;

      // tab title
      this.titleService.setTitle(data.name + " | Find Dining Scarborough");

      // displayed phone
      var phone: string = String(this.restaurantDetails.phone);
      this.displayed_phone = phone != 'null' ? "(" + phone.slice(0, 3) + ") " + phone.slice(3, 6) + " " + phone.slice(6, 10) : '';

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
          if (this.serviceCount < 4) {
            this.firstFourServices = this.serviceList;
          }
          this.serviceCount += 1;
        }
      }

      // payment list
      //this.paymentList = this.restaurantDetails.payment_methods.toString().split(',').join(', ') + " Accepted";
      this.paymentList = this.restaurantDetails.payment_methods.toString().split(',').join(', ');

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
        this.slides.push({ url: url.replace(' ', '%20') });
      }

      this.videoId = this.getVideoId(this.restaurantDetails.restaurant_video_url);
    }, (error) => {
      this.error = true;
    });

    this.getPendingOrApprovedDishes(this.restaurantId).subscribe((data) => {
      this.restaurantMenu = data.Dishes;
      for (let dish of this.restaurantMenu) {
        dish.type = 'dish';
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

  gotoRestaurant() {
    this.router.navigate(['/all-listings'], { queryParams: {GEO_location: this.restaurantDetails.GEO_location} }).then(() => {
      this.reload();
    })
  }

  /**
   * Retrieves the restaurant from the database, either the pending
   * one or the approved one depending on the role
   *
   * @param id - the restaurant's id
   * @returns the retrieved restaurant record
   */
  getPendingOrApprovedRestaurant(id) {
    if (this.role == 'RO' && !id) {
      return this.restaurantService.getPendingRestaurant();
    } else {
      return this.restaurantService.getApprovedRestaurant(id);
    }
  }

  /**
   * Retrieves the restaurant dishes from the database
   *
   * @param id - the restaurant's id
   * @returns the restaurant dishes
   */
  getPendingOrApprovedDishes(id) {
    if (this.role == 'RO' && !id) {
      return this.restaurantService.getPendingRestaurantFood();
    } else {
      return this.restaurantService.getApprovedRestaurantFood(id);
    }
  }

  /**
   * Retrieves the user-friendly value of priceLevel
   * @param priceLevel - the price level (LOW, MID, HIGH, EXHIGH)
   * @returns the user-friendly value of priceLevel
   */
  getPricepoint(priceLevel: string) {
    // priceLevels: LOW, MID, HIGH, EXHIGH
    // return: $, $$, $$$, $$$$
    for (let p of this.pricepoints) {
      if (p["value"] == priceLevel) {
        return p["key"];
      }
    }
  }

  /**
   * Redirects to the restaurant-setup page
   */
  editRestaurant() {
    this.router.navigate(['/restaurant-setup']);
  }

  /**
   * Redirects to the menu-edit page
   */
  editMenu() {
    this.router.navigate(['/menu-edit']);
  }

  /**
   * Redirects to the previous page
   */
  goBack() {
    this.location.back();
    this.reload();
    //this.router.navigate(['/all-listings']);
  }

  openExternalMenu() {
    window.open(this.restaurantDetails.full_menu_url, '_blank')
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

  /**
   * Opens the edit modal form
   * @param content - the modal to open
   */
  openEditModal(content) {
    this.validator.clearAllErrors();
    this.draftValidator.clearAllErrors();
    this.modalRef = this.modalService.open(content, { size: 's' });
    this.newFile = false;
  }

  /**
   * Gets the selected image file
   * @param event - the object containing the image file
   */
  onStoryImgSelect(event) {
    if (event.target.files.length > 0) {
      const file = event.target.files[0];
      this.uploadStoryImgForm.get('file').setValue(file);
      this.newFile = true;
    }
  }

  /**
   * Gets the selected video file
   * @param event - the object containing the video file
   */
  onVideoFileSelect(event) {
    if (event.target.files.length > 0) {
      const file = event.target.files[0];
      this.uploadVideoForm.get('file').setValue(file);
      this.submitVideoAllowed = true;
    }
  }

  /**
   * Gets the selected image file(s) from the restaurant carousel
   * @param event - the object containing the restaurant carousel image files
   */
  onImageFileSelect(event) {
    if (event.target.files.length > 0) {
      const file = event.target.files;
      this.uploadImageForm.get('file').setValue(file);
      this.newFile = true;
    }
  }

  /**
   * Uploads the restaurant story image
   */
  onSubmitStoryImg() {
    const formData = new FormData();
    formData.append('media_file', this.uploadStoryImgForm.get('file').value);

    this.mediaService.uploadRestaurantMedia(formData, 'IMAGE', 'cover_photo_url', 'False').subscribe((data) => {
      this.reload();
    })
    this.modalRef.close();
  }

  /**
   * Sets the full menu url of the restaurant
   */
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

  /**
   * Uploads the restaurant's video
   */
  onSubmitVideo() {
    const formData = new FormData();
    formData.append('media_type', 'VIDEO');
    formData.append('save_location', 'restaurant_video_url');
    formData.append('submit_for_approval', 'False');

    let info = {
      restaurant_video_desc: (<HTMLInputElement>document.getElementById('video_desc')).value,
    }
    this.draftValidator.clearAllErrors();
    var failFlag = this.draftValidator.validateAll(info, (key) => {
      this.draftValidator.setError(key)
    });

    if (this.uploadMethod == 'Upload .mp4 video file') {

      if (!failFlag) {
        formData.append('media_file', this.uploadVideoForm.get('file').value);
        this.mediaService.uploadRestaurantMedia(formData, 'VIDEO', 'restaurant_video_url', 'False').subscribe((data) => {
          this.chooseUpdateAPI(this.restaurantDetails.status, info).subscribe((data) => {
            this.modalRef.close();
            alert("Changes to restaurant are now saved as draft");
            this.reload();
          });
        });
      } else {
        alert("Please ensure all fields are entered in correctly");
      }

    } else if (this.uploadMethod == 'YouTube video link') {
      let linkInfo = {
        link: (<HTMLInputElement>document.getElementById('youtube_link')).value
      };

      this.validator.clearAllErrors();
      failFlag = failFlag || this.validator.validateAll(linkInfo, (key) => this.validator.setError(key));

      if (!failFlag) {
        formData.append('media_link', linkInfo.link);
        this.mediaService.uploadRestaurantMedia(formData, 'VIDEO', 'restaurant_video_url', 'False').subscribe((data) => {
          this.chooseUpdateAPI(this.restaurantDetails.status, info).subscribe((data) => {
            this.modalRef.close();
            alert("Changes to restaurant are now saved as draft");
            this.reload();
          });
        });
      } else {
        alert("Please ensure all fields are entered in correctly");
      }
    }
  }

  /**
   * Uploads or deletes the restaurant carousel image(s)
   */
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

  /**
   * Deteremines if video to be uploaded is a youtube link or mp4 file
   */
  updateUploadMethod() {
    this.uploadMethod = (<HTMLInputElement>document.getElementById('upload_method')).value;
    this.submitVideoAllowed = false;
  }

  /**
   * Determines if the restaurant carousel images are to be uploaded or deleted
   */
  updateAddOrRemove() {
    this.addOrRemove = (<HTMLInputElement>document.getElementById('add_or_remove')).value;
    if (this.addOrRemove == 'Delete from existing images') {
      this.imageUrls = Object.assign([], this.restaurantDetails.restaurant_image_url);
      this.imageUrlsToDelete = [];
    }
  }

  /**
   * Gets the youtube video id of the restaurant video
   * @param link - the restaurant video url
   * @returns The id of the restaurant youtube video
   */
  getVideoId(link: string) {
    return (getVideoId(link) as { id, service }).id;
  }

  /**
   * Removes the image url from the list of restaurant carousel images
   * @param imgUrl - the url of the restaurant carousel image to delete
   */
  deleteImage(imgUrl: string) {
    if (imgUrl != undefined && !this.imageUrlsToDelete.includes(imgUrl)) {
      this.imageUrlsToDelete.push(imgUrl);
      this.imageUrls.forEach((url, index) => {
        if (url == imgUrl) delete this.imageUrls[index];
      });
    }
  }

  /**
   *
   * @param status - the restaurant's status
   * @param info - the restaurant info
   * @returns the updated restaurant record
   */
  chooseUpdateAPI(status: string, info: Object): Observable<any> {
    info['email'] = this.restaurantDetails.email;
    info['name'] = this.restaurantDetails.name;
    info['address'] = this.restaurantDetails.address;
    info['postalCode'] = this.restaurantDetails.postalCode;
    info['owner_first_name'] = this.restaurantDetails.owner_first_name;
    info['owner_last_name'] = this.restaurantDetails.owner_last_name;
    return this.restaurantService.updateRestaurantDraft(info);

    // switch (status) {
    //   case 'In_Progress':
    //     return this.restaurantService.updateRestaurantDraft(info);
    //   default:
    //     info['years'] = this.restaurantDetails.years;
    //     info['phone'] = this.restaurantDetails.phone;
    //     info['pricepoint'] = this.restaurantDetails.pricepoint;
    //     info['bio'] = this.restaurantDetails.bio;
    //     info['open_hours'] = this.restaurantDetails.open_hours;
    //     info['payment_methods'] = this.restaurantDetails.payment_methods;
    //     info['offer_options'] = this.restaurantDetails.offer_options;
    //     return this.restaurantService.insertRestaurantApproval(info);
    // }
  }


  /**
   * Performs action to retrieve the 5 or less nearest restaurants
   */
  getNearbyRestaurants() {
    this.userService.getNearbyRestaurants().subscribe((restaurants) => {
      for (let entry of restaurants) {
        let restaurant = entry.restaurant
        this.nearbyRestaurants.push({
          name: restaurant.name,
          cuisinePrice: restaurant.cuisines[0] + " - " + restaurant.pricepoint,
          imgUrl: restaurant.logo_url,
          _id: restaurant._id
        })
      }
    });
  }

}
