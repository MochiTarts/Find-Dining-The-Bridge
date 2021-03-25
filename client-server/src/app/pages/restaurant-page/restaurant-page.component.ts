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

      // console.log(user);
    }

    this.restaurantId = this.route.snapshot.queryParams.restaurantId || this.userId;

    if (this.restaurantId == this.route.snapshot.queryParams.restaurantId) this.isQueryRestaurant = true;

    this.getPendingOrApproved(this.restaurantId).subscribe((data) => {
      // console.log(data);
      this.restaurantDetails = data;

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
    })


    // this.restaurantDetails = {
    //   _id: "603554df682689f2764ca4a2",
    //   name: "Min's Restaurant",
    //   years: 10,
    //   address: "1265 Military Trail",
    //   streetAddress2: "",
    //   streetAddress3: "",
    //   postalCode: "M1C 1A4",
    //   phone: 1231231234,
    //   email: "ahar@plussmail.com",
    //   pricepoint: "EXHIGH",
    //   cuisines: [
    //       "American"
    //   ],
    //   offer_options: [
    //       "Delivery",
    //       "Pick-up",
    //       "Dine-in",
    //       "Meal Kits",
    //       "Catering",
    //       "Cash only",
    //       "Gluten-free Options"
    //   ],
    //   dineinPickupDetails: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas ac dui non urna tempor luctus et eu lorem. Proin ac dapibus dolor. Proin pellentesque leo nunc, sit amet vulputate justo dictum nec. Etiam nisi metus, sollicitudin quis nibh non, viverra gravida tellus. Suspendisse potenti. Nullam ornare sit amet turpis a mattis. Nullam sit amet nisl at dolor tempus facilisis. Vestibulum eu faucibus neque. Mauris id commodo nisi, vel dapibus ipsum. Etiam convallis eros felis, et suscipit nisi pharetra ut. Duis ac nisi id risus tempus vehicula.",
    //   deliveryDetails: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas ac dui non urna tempor luctus et eu lorem. Proin ac dapibus dolor. Proin pellentesque leo nunc, sit amet vulputate justo dictum nec. Etiam nisi metus, sollicitudin quis nibh non, viverra gravida tellus. Suspendisse potenti. Nullam ornare sit amet turpis a mattis. Nullam sit amet nisl at dolor tempus facilisis. Vestibulum eu faucibus neque. Mauris id commodo nisi, vel dapibus ipsum. Etiam convallis eros felis, et suscipit nisi pharetra ut. Duis ac nisi id risus tempus vehicula.",
    //   locationNotes: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas ac dui non urna tempor luctus et eu lorem. Proin ac dapibus dolor. Proin pellentesque leo nunc, sit amet vulputate justo dictum nec. Etiam nisi metus, sollicitudin quis nibh non, viverra gravida tellus. Suspendisse potenti. Nullam ornare sit amet turpis a mattis. Nullam sit amet nisl at dolor tempus facilisis. Vestibulum eu faucibus neque. Mauris id commodo nisi, vel dapibus ipsum. Etiam convallis eros felis, et suscipit nisi pharetra ut. Duis ac nisi id risus tempus vehicula.",
    //   web_url: "",
    //   facebook: "https://www.facebook.com/finddiningscarborough/",
    //   twitter: "https://twitter.com/FDscarborough",
    //   instagram: "https://www.instagram.com/finddiningscarborough/",
    //   bio: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas ac dui non urna tempor luctus et eu lorem. Proin ac dapibus dolor. Proin pellentesque leo nunc, sit amet vulputate justo dictum nec. Etiam nisi metus, sollicitudin quis nibh non, viverra gravida tellus. Suspendisse potenti. Nullam ornare sit amet turpis a mattis. Nullam sit amet nisl at dolor tempus facilisis. Vestibulum eu faucibus neque. Mauris id commodo nisi, vel dapibus ipsum. Etiam convallis eros felis, et suscipit nisi pharetra ut. Duis ac nisi id risus tempus vehicula.",
    //   GEO_location: "{'lat': 43.7825084, 'lng': -79.1853174}",
    //   cover_photo_url: "https://storage.googleapis.com/test-storage-nog/FILE-rgxlmwhtkx-2021-03-03 18:02:44.675947.png",
    //   logo_url: "https://storage.googleapis.com/default-assets/logo.jpg",
    //   restaurant_video_url: "https://storage.googleapis.com/test-storage-nog/FILE-vsphyaetao-2021-02-23 21:57:17.919193.mp4",
    //   restaurant_image_url: [
    //       "https://storage.googleapis.com/test-storage-nog/FILE-hojjovlzvu-2021-02-23 19:41:23.457993.png",
    //       "https://storage.googleapis.com/test-storage-nog/FILE-aekyxbzwoe-2021-02-23 19:41:27.150875.png",
    //       "https://storage.googleapis.com/test-storage-nog/FILE-wzwcrdqyzw-2021-02-23 19:41:28.117848.png",
    //       "https://storage.googleapis.com/test-storage-nog/FILE-ahlssfibfa-2021-02-23 19:41:28.834423.png",
    //       "https://storage.googleapis.com/test-storage-nog/FILE-ttgmlbwiud-2021-02-23 19:41:29.774578.png",
    //       "https://storage.googleapis.com/test-storage-nog/FILE-zxnfrcxetu-2021-02-23 19:41:32.839115.png",
    //       "https://storage.googleapis.com/test-storage-nog/FILE-gorfjgjbze-2021-02-23 19:41:34.429799.png",
    //       "https://storage.googleapis.com/test-storage-nog/FILE-ippzznymjk-2021-02-23 19:41:35.548928.png"
    //   ],
    //   owner_first_name: [
    //       "Min Qi"
    //   ],
    //   owner_last_name: [
    //       "Zhang"
    //   ],
    //   owner_preferred_name: [
    //       "Min"
    //   ],
    //   owner_story: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas ac dui non urna tempor luctus et eu lorem. Proin ac dapibus dolor. Proin pellentesque leo nunc, sit amet vulputate justo dictum nec. Etiam nisi metus, sollicitudin quis nibh non, viverra gravida tellus. Suspendisse potenti. Nullam ornare sit amet turpis a mattis. Nullam sit amet nisl at dolor tempus facilisis. Vestibulum eu faucibus neque. Mauris id commodo nisi, vel dapibus ipsum. ",
    //   owner_picture_url: "https://storage.googleapis.com/test-storage-nog/FILE-ztawvdypdr-2021-02-23 19:17:51.665567.png",
    //   categories: [
    //       "Signature Dish",
    //       "Popular Dish"
    //   ],
    //   status: "Pending",
    //   sysAdminComments: "",
    //   open_hours: "Monday - 9:00am-5:00pm\nTuesday - 9:00am-5:00pm\nWednesday - 9:00am-5:00pm\nThursday - 9:00am-5:00pm\nFriday - 9:00am-5:00pm\nSaturday - 9:00am-5:00pm\nSunday - 9:00am-5:00pm",
    //   payment_methods: [
    //       "Debit",
    //       "Credit",
    //       "Cash"
    //   ],
    //   full_menu_url: "https://thierrysans.me/CSCC09/lectures/02/slides/C09-Javascript.pdf",
    //   approved_once: false
    // };


  }

  getPendingOrApproved(id) {
    if (this.authService.isLoggedIn && this.role == 'RO' && !this.isQueryRestaurant) {
      return this.restaurantService.getPendingRestaurant();
    } else {
      return this.restaurantService.getApprovedRestaurant(id);
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
    let currentUrl = this.router.url;
    this.router.routeReuseStrategy.shouldReuseRoute = () => false;
    this.router.onSameUrlNavigation = 'reload';
    this.router.navigate([currentUrl]);
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
    this.modalRef.close();
    console.log("story image submitted");
  }

  onSubmitFullMenu() {
    this.modalRef.close();
    console.log("full menu url submitted");
  }

  onSubmitVideo() {
    this.modalRef.close();
    console.log("video submitted");
  }

  onSubmitImage() {
    this.modalRef.close();
    console.log("restaurant images submitted");
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

}
