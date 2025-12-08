// src/components/layout/SocialLink.jsx

import './SocialLink.scss';
import { FaFacebookF, FaInstagram, FaYoutube } from "react-icons/fa";
import Logo from '../../assets/images/Aura.png';

const SocialLink = () => {
  return (
    <section className="SocialLink">
      <div className="SocialLink__container">

        {/* 1. Phần Top (Logo, Email, Socials) */}
        <div className="SocialLink__top">
          <img src={Logo} alt="Aura Logo" className="SocialLink__logo" />
          <p className="SocialLink__email-label">Email:</p>
          <a href="mailto:sale@auracraft.com" className="SocialLink__email-link">
            sale@auracraft.com
          </a>

          <div className="SocialLink__socials">
            <a href="#" className="social-icon">
              <FaFacebookF />
            </a>
            <a href="#" className="social-icon">
              <FaInstagram />
            </a>
            <a href="#" className="social-icon">
              <FaYoutube />
            </a>
          </div>
        </div>
      </div>

      {/* 2. Phần line */}
      <div className="footer__divider"></div>

      <div className="SocialLink__container">
        {/* 3. Phần Bottom (Links) */}
        <div className="SocialLink__bottom">
          <a href="/san-pham" className="SocialLink-link">
            <span>Sản phẩm</span>
            <span>&gt;</span>
          </a>
          <a href="/ve-chung-toi" className="SocialLink-link">
            <span>Về chúng tôi</span>
            <span>&gt;</span>
          </a>
          <a href="/lien-he" className="SocialLink-link">
            <span>Liên hệ</span>
            <span>&gt;</span>
          </a>
        </div>

      </div>
    </section>
  );
};

export default SocialLink;