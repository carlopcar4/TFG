# FROM ruby:3.2.2

# # Instala Node 20 y Yarn
# RUN apt-get update -qq && \
#     apt-get install -y curl gnupg2 postgresql-client && \
#     curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
#     apt-get install -y nodejs && \
#     npm install --global yarn

# WORKDIR /app
# COPY . .

# # Gems
# RUN gem install bundler && bundle install

# # NPM/Yarn (borra el package-lock si existe para evitar el warning)
# RUN rm -f package-lock.json && yarn install --check-files && yarn add uc.micro@1.0.6 --ignore-scripts && yarn add graphql@16.9.0 --ignore-scripts

# # Compilamos assets
# RUN bundle exec rails shakapacker:compile

# CMD ["bin/rails", "server", "-b", "0.0.0.0"]


FROM ruby:3.2.2

RUN apt-get update -qq && \
    apt-get install -y curl gnupg2 postgresql-client && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    npm install --global yarn

WORKDIR /app
COPY . .

RUN gem install bundler && bundle install

RUN rm -f package-lock.json && yarn install --check-files

RUN bundle exec rails shakapacker:compile

CMD ["bin/rails", "server", "-b", "0.0.0.0"]
