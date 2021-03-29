import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-partner-card',
  templateUrl: './partner-card.component.html',
  styleUrls: ['./partner-card.component.scss']
})
export class PartnerCardComponent implements OnInit {
  @Input() partner: any;

  constructor() { }

  ngOnInit(): void {
  }

}
