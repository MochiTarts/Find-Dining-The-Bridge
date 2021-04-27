import { Component, OnInit } from '@angular/core';
import { Title } from '@angular/platform-browser';

@Component({
  selector: 'app-account-removal-instruction',
  templateUrl: './account-removal-instruction.component.html',
  styleUrls: ['./account-removal-instruction.component.scss']
})
export class AccountRemovalInstructionComponent implements OnInit {

  constructor(
    private titleService: Title,
  ) { }

  ngOnInit(): void {
    this.titleService.setTitle("Terms of Service | Find Dining Scarborough");
  }

}
