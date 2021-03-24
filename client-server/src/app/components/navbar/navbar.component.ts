import { Component, OnInit } from '@angular/core';
import { TokenStorageService } from '../../_services/token-storage.service';
import { UserService } from '../../_services/user.service';
import { AuthService } from '../../_services/auth.service';
import { Router } from '@angular/router';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import {
  faUserCircle,
  faMapMarkerAlt,
} from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss'],
})
export class NavbarComponent implements OnInit {
  title: string = 'Find Dining Scarborough';
  email: string = "jenny100.yu@gmail.com"

  restaurantId: string = '';
  userId: string = '';
  userAddress: string = '';
  modalRef: any;
  faUserCircle = faUserCircle;
  faMapMarkerAlt = faMapMarkerAlt;

  private role: string = 'BU';
  username?: string;

  constructor(
    private userService: UserService,
    public authService: AuthService,
    public tokenStorageService: TokenStorageService,
    private router: Router,
    private modalService: NgbModal
  ) { }



  ngOnInit(): void {
    if (this.authService.isLoggedIn()) {
      const user = this.tokenStorageService.getUser();
      this.role = user.role;
      this.username = user.username;
    }
  }


  reload() {
    window.location.reload();
  }

  browse() {
    this.router.navigate(['/all-listings']).then(() => {
      setTimeout(function () {
        //window.location.reload();
      }, 100);
    });
  }

  home() {
    this.router.navigate(['/']).then(() => {
      setTimeout(function () {
        //window.location.reload();
      }, 100);
    })
  }


  owners() {
    this.router.navigate(['/all-owners']).then(() => {
      setTimeout(function () {
        //window.location.reload();
      }, 100);
    });
  }

  favourites() {
    this.router.navigate(['/favourites']).then(() => {
      setTimeout(function () {
        //window.location.reload();
      }, 100);
    });
  }

  profile() {
    this.router.navigate(['/profile']).then(() => {
      setTimeout(function () {
        //window.location.reload();
      }, 100);
    });
  }

  restaurant() {
    this.router.navigate(['/restaurant'])
  }

  accountSetting() {
    this.router.navigate(['/account-setting']).then(() => {
      setTimeout(function () {
        //window.location.reload();
      }, 100);
    });
  }

  newsletter() {
    this.router.navigate(['/newsletter']).then(() => {
      setTimeout(function () {
        //window.location.reload();
      }, 100);
    });
  }

  restaurantSetup() {
    this.router.navigate(['/restaurant-setup'])
  }

  openModal(content) {
    this.modalRef = this.modalService.open(content);
  }

  goToSetup() {
    this.modalRef.close();
    this.router.navigate(['/restaurant-setup']);
  }

  onLoginRegisterClicked() {
    if (this.authService.isLoggedIn()) {
      this.logout();
    } else {
      this.router.navigate(['/login']);
    }
  }

logout(): void {
  this.authService.updateLoginStatus(false);
  this.tokenStorageService.signOut();
  this.router.navigate(['/']).then(() => {
    window.location.reload()
  });
}

}
