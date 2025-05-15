# class CouncilsController < ApplicationController
#   include Rails.application.routes.url_helpers
#   skip_before_action :verify_authenticity_token

#   def index
#     @councils = Council.all
#     render json: @councils.as_json(methods: :decidim_url)
#   end

#   def show
#     @council = Council.find(params[:id])
#     if @council.logo.attached? and  @council.banner.attached?
#       logo_url = url_for(@council.logo)
#       banner_url = url_for(@council.banner)
#       t = @council.as_json.merge(logo_url: logo_url, banner_url: banner_url)
#       render json: t, status: :accepted
#       methods: :decidim_url
#     else
#       render json: @council
#     end
#   end


#   def create
#     @council = Council.new(council_params)
#     @council.logo.attach(params[:logo])
#     @council.banner.attach(params[:banner])

#     if @council.save
#       DeployCouncilService.new(@council).call
#       if @council.logo.attached? and  @council.banner.attached?
#         logo_url=url_for(@council.logo)
#         banner_url=url_for(@council.banner)
#         t = @council.as_json.merge(logo_url: logo_url, banner_url: banner_url)

#         render json: t, status: :created
#       else
#         render json: @council, status: :created
#       end
#     else
#       render json: @council.errors, status: :unprocessable_entity
#     end
#   end


#   def update
#     begin
#       @council = Council.find(params[:id])
#       if @council.update(params.permit(:name, :province, :population, :multi_tenant, collaborations: [], services: []))
#         render json: @council, status: :ok
#       else 
#         render json: @council, status: :no_content
#       end
#     rescue Exception => e
#       Rails.logger.error(e)
#       render json: @council.errors, status: :bad_request
#     end
#   end


#   def deploy
#     @council = Council.find(params[:id])
#     if ['stopped', 'pending'].include?(@council.status)
#       begin
#         DeployCouncilService.new(@council).call
#         @council.update(status: 'running')
#         render json: {message: "Desplegado correctamente"}
#       rescue Exception => e
#         Rails.logger.error(e)
#         render json: @council.errors, status: :bad_request
#       end
#     else
#       begin
#         StopCouncilService.new(@council).call
#         @council.update(status: 'stopped')
#         render json: {message: "Instancia parada correctamente"}
#       rescue Exception => e
#         Rails.logger.error(e)
#         render json: @council.errors, status: :bad_request
#       end
#     end
#   end

#   def reset
#     @council = Council.find(params[:id])
#     if ['running'].include?(@council.status)
#       begin
#         ResetCouncilService.new(@council).call
#         render json: {message: "Reinicio completado"}
#       rescue Exception => e
#         Rails.logger.error(e)
#         render json: @council.errors, status: :bad_request
#       end
#     end
#   end


#   def destroy
#     @council = Council.find(params[:id])
#     if @council.destroy
#       render json: {message: "Municipio eliminado correctamente" }
#     else
#       render json: @council.errors, status: :not_found
#     end
#   end

#   private

#   def council_params
#     params.permit(:name, :province, :population, :multi_tenant, collaborations: [], services: [])
#   end


# end

# app/controllers/councils_controller.rb
class CouncilsController < ApplicationController
  include Rails.application.routes.url_helpers
  skip_before_action :verify_authenticity_token

  # GET /councils
  def index
    councils = Council.all
    render json: councils.as_json(methods: :decidim_url)
  end

  # GET /councils/:id
  def show
    council = Council.find(params[:id])

    payload = council.as_json(methods: :decidim_url)
    payload[:logo_url]   = url_for(council.logo)   if council.logo.attached?
    payload[:banner_url] = url_for(council.banner) if council.banner.attached?

    render json: payload, status: :accepted
  end

  # POST /councils
  def create
    council = Council.new(council_params)
    council.logo.attach(params[:logo])
    council.banner.attach(params[:banner])

    if council.save
      DeployCouncilService.new(council).call
      payload = council.as_json(methods: :decidim_url)
      payload[:logo_url]   = url_for(council.logo)   if council.logo.attached?
      payload[:banner_url] = url_for(council.banner) if council.banner.attached?
      render json: payload, status: :created
    else
      render json: council.errors, status: :unprocessable_entity
    end
  end

  # PATCH /councils/:id
  def update
    council = Council.find(params[:id])

    if council.update(params.permit(:name, :province, :population, :multi_tenant, collaborations: [], services: []))
      render json: council.as_json(methods: :decidim_url), status: :ok
    else
      render json: council.errors, status: :unprocessable_entity
    end
  end

  # PATCH /councils/:id/deploy   (arranca o para)
  def deploy
    council = Council.find(params[:id])

    if %w[stopped pending].include?(council.status)
      DeployCouncilService.new(council).call
      council.update(status: "running")
      render json: { message: "Desplegado correctamente" }
    else
      StopCouncilService.new(council).call
      council.update(status: "stopped")
      render json: { message: "Instancia parada correctamente" }
    end
  rescue => e
    Rails.logger.error(e)
    render json: council.errors, status: :bad_request
  end

  # PATCH /councils/:id/reset
  def reset
    council = Council.find(params[:id])

    if council.status == "running"
      ResetCouncilService.new(council).call
      render json: { message: "Reinicio completado" }
    else
      render json: { message: "La instancia no está en ejecución" }, status: :unprocessable_entity
    end
  rescue => e
    Rails.logger.error(e)
    render json: council.errors, status: :bad_request
  end

  # DELETE /councils/:id
  def destroy
    council = Council.find(params[:id])

    if council.destroy
      render json: { message: "Municipio eliminado correctamente" }
    else
      render json: council.errors, status: :not_found
    end
  end

  private

  def council_params
    params.permit(:name, :province, :population, :multi_tenant, collaborations: [], services: [])
  end
end
