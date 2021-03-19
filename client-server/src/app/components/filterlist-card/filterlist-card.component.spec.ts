import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { FilterlistCardComponent } from './filterlist-card.component';

describe('FilterlistCardComponent', () => {
  let component: FilterlistCardComponent;
  let fixture: ComponentFixture<FilterlistCardComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ FilterlistCardComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FilterlistCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
