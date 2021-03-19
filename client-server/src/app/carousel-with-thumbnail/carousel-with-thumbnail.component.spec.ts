import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CarouselWithThumbnailComponent } from './carousel-with-thumbnail.component';

describe('CarouselWithThumbnailComponent', () => {
  let component: CarouselWithThumbnailComponent;
  let fixture: ComponentFixture<CarouselWithThumbnailComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CarouselWithThumbnailComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CarouselWithThumbnailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
