class Council < ApplicationRecord
  belongs_to :decidim_process, class_name: "Decidim::ParticipatoryProcess", optional: true

  has_one_attached :logo
  has_one_attached :banner
  
  before_create :pending

  def decidim_url
    "http://#{name.parameterize}.localhost.3000"
  end

  private
  def pending
    self.status = 'pending'
  end
end
