import { AfterViewInit, Component, OnInit } from '@angular/core';
import { UserService } from './_services/user.service';
import { SpinnerVisibilityService } from 'ng-http-loader';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit, AfterViewInit {
  private role: string = 'BU';
  isLoggedIn = false;
  showROBoard = false;
  username?: string;

  constructor(
    private userService: UserService,
    private spinner: SpinnerVisibilityService
  ) {}

  ngOnInit(): void {
    this.spinner.show();
    if (!document.cookie.split('; ').find(row => row.startsWith('csrftoken'))) {
      this.userService.setCSRFToken().subscribe(
        data => {
        },
        err => {
        }
      )
    }
  }

  ngAfterViewInit(): void {
    setTimeout(() => {
      this.spinner.hide();
    }, 1000)
  }

}
