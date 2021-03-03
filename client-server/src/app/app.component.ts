import { Component, OnInit } from '@angular/core';
import { TokenStorageService } from './_services/token-storage.service';
import { UserService } from './_services/user.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  private role: string = 'BU';
  isLoggedIn = false;
  showROBoard = false;
  username?: string;

  constructor(private userService: UserService, private tokenStorageService: TokenStorageService) { }

  ngOnInit(): void {
    if (!document.cookie.split('; ').find(row => row.startsWith('csrftoken'))) {
      this.userService.setCSRFToken().subscribe(
        data => {
        },
        err => {
        }
      )
    }


    this.isLoggedIn = !!this.tokenStorageService.getToken();

    if (this.isLoggedIn) {
      const user = this.tokenStorageService.getUser();
      console.log(user)
      this.role = user.role;

      this.showROBoard = this.role == 'RO';

      this.username = user.username;
    }
  }

  logout(): void {
    this.tokenStorageService.signOut();
    window.location.reload();
  }
}