def template(code):
    return """
        <html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Devtranet - Email Verification</title>
    <style>
      @import url("https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700;900&display=swap");
​
      body,
      html {
        width: 100%;
        height: 100%;
        margin: 0;
        padding: 0;
        font-family: "Roboto", sans-serif;
        font-weight: 400;
        color: #000000;
        line-height: 1.5;
      }
​
      * {
        margin: 0;
        padding: 0;
      }
​
      .email-verification-template {
        width: 520px;
        /* height: 525px; */
        background: #d9d9d9;
        border-radius: 3px;
        padding: 22px 32px 23px 36px;
      }
​
      .footer-text {
        font-size: 12px;
        line-height: 14px;
        text-align: center;
        margin-top: 19px;
        font-weight: 300;
      }
​
      .main {
        background: #ffffff;
        width: 452px;
        /* height: 445px; */
        padding: 31px 27px 26px 27px;
      }
​
      .logo {
        width: 200px;
        height: 42.62px;
        margin-bottom: 18.38px;
      }
​
      .heading-2022 {
        font-weight: 700;
        font-size: 24px;
        line-height: 28px;
        color: #5f6fee;
      }
      .text-2022 {
        font-size: 16px;
        line-height: 19px;
        margin: 26px 0 20px 0;
      }
      .code-wrapper {
        height: 62px;
        /* width: 398px; */
        background: #d9d9d9;
        border-radius: 3px;
        padding: 0 22px;
      }
​
      .code-2022 {
        font-weight: 700;
        font-size: 36px;
        line-height: 42px;
        color: #5f6fee;
        padding: 10px 0;
      }
​
      .description-2022 {
        font-size: 16px;
        line-height: 19px;
        width: 311px;
        margin: 15px 0 57px 0;
      }
​
      .stay-connected {
        font-weight: 700;
        font-size: 14px;
        line-height: 16px;
        margin-bottom: 25px;
        text-align: center;
      }
​
      .socials {
        /* margin: 0 100px 0 108px; */
        display: flex;
        justify-content: center;
        align-items: center;
        margin-left: 100px;
      }
​
      .social_icon {
        margin: 0 26px;
      }
​
      .social_icon1 {
        margin-right: 26px;
      }
​
      .social_icon4 {
        margin-left: 26px;
      }
​
      .social_icon > img,
      .social_icon1 > img,
      .social_icon4 > img {
        width: 28px;
        height: 28px;
      }
​
      @media screen and (max-width: 428px) {
        .socials {
          margin-left: 6px;
        }
        .social_icon {
          margin: 0 14px;
        }
				.social_icon1 {
					margin-right: 14px;
				}
​
				.social_icon4 {
					margin-left: 14px;
				}
        .main {
          max-width: 452px;
          width: auto;
        }
        .email-verification-template {
          max-width: 520px;
          width: auto;
        }
        .description-2022 {
          max-width: 311px;
          width: auto;
        }
      }
    </style>
    <!-- Global site tag (gtag.js) - Google Analytics -->
    <script
      async
      src="https://www.googletagmanager.com/gtag/js?id=G-YS06M4G9WJ"
    ></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag() {
        dataLayer.push(arguments);
      }
      gtag("js", new Date());
​
      gtag("config", "G-YS06M4G9WJ");
    </script>
  </head>
​
  <body>
    <div class="email-verification-template">
      <div class="main">
        <div class="content-top">
          <img
            class="logo"
            src="https://devtranet.tech/assets/logo.png"
            alt="devtranet_logo"
          />
        </div>
        <div class="content-main">
          <p class="heading-2022">Verification Code</p>
          <p class="text-2022">Here is your verification code:</p>
          <div class="code-wrapper">
            <p class="code-2022">%s</p>
          </div>
          <p class="description-2022">
            Use it to continue creating your account, it expires in 15 minutes.
          </p>
        </div>
        <div class="content-bottom">
          <p class="stay-connected">Stay Connected!</p>
          <div class="socials">
            <a
              class="social_icon1"
              href="https://www.linkedin.com/company/devtranet"
              target="_blank"
              rel="noreferrer"
              ><img
                src="https://devtranet.tech/assets/email-template/img1.png"
                alt="linkedin icon"
            /></a>
            <a
              class="social_icon"
              href="https://twitter.com/devtranet"
              target="_blank"
              rel="noreferrer"
              ><img
                src="https://devtranet.tech/assets/email-template/img2.png"
                alt="twitter icon"
            /></a>
            <a class="social_icon" href="/" target="_blank" rel="noreferrer"
              ><img
                src="https://devtranet.tech/assets/email-template/img3.png"
                alt="youtube icon"
            /></a>
            <a
              class="social_icon4"
              href="https://facebook.com/devtranet"
              target="_blank"
              rel="noreferrer"
              ><img
                src="https://devtranet.tech/assets/email-template/img4.png"
                alt="facebook icon"
            /></a>
          </div>
        </div>
      </div>
      <div class="footer">
        <p class="footer-text">
          Ⓒ Devtranet, the official network for Developers.
        </p>
      </div>
    </div>
  </body>
</html>
""" % (
        code,
    )
