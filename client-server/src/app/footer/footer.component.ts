import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import {
  faFacebookSquare,
  faTwitter,
  faInstagram,
} from '@fortawesome/free-brands-svg-icons';

@Component({
  selector: 'app-footer',
  templateUrl: './footer.component.html',
  styleUrls: ['./footer.component.scss'],
})
export class FooterComponent implements OnInit {
  faFacebook = faFacebookSquare;
  faTwitter = faTwitter;
  faInstagram = faInstagram;

  constructor(
    private router: Router
  ) {}

  ngOnInit(): void {}

  onBecomePartnerClicked() {
    this.router.navigate(['/login']);
  }
}
