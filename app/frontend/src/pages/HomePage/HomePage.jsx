// 1. Import Swiper
import { Swiper, SwiperSlide } from 'swiper/react';
import { Pagination, Autoplay } from 'swiper/modules'; 

// 2. Import CSS của Swiper
import 'swiper/css';
import 'swiper/css/pagination';
import 'swiper/css/autoplay';

// 3. Import SASS chính của trang
import './HomePage.scss';

// 4. Import các phần
import SlideAura from './SlideAura';
import SlideFiber from './SlideFiber';
import SlideFair from './SlideFair';
import FeaturedProducts from './FeaturedProducts';
import OurJourney from './OurJourney';
import Commitments from './Commitments';
import SocialLink from '../../components/layout/SocialLink';

const HomePage = () => {
  return (
    <div className="homepage">

      <Swiper
        modules={[Pagination, Autoplay]} // Kích hoạt mô-đun
        pagination={{ clickable: true }}  // Cho phép bấm vào dấu chấm
        autoplay={{ delay: 3000, disableOnInteraction: true }} // Tự động trượt
        loop={true} // Lặp vô hạn
        className="hero-swiper"
      >
        <SwiperSlide>
          <SlideAura />
        </SwiperSlide>

        <SwiperSlide>
          <SlideFiber />
        </SwiperSlide>

        <SwiperSlide>
          <SlideFair />
        </SwiperSlide>

      </Swiper>

      <FeaturedProducts />

      <OurJourney />

      <Commitments />

      <SocialLink />

    </div>
  );
};

export default HomePage;